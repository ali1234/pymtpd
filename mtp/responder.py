from __future__ import print_function

import io
import shutil
import queue

import logging
logger = logging.getLogger(__name__)

from mtp.exceptions import MTPError
from mtp.device import DeviceInfo, DeviceProperties, DevicePropertyCode
from mtp.packets import MTPOperation, MTPResponse, MTPData, MTPEvent, DataType, OperationCode, EventCode
from mtp.watchmanager import WatchManager
from mtp.handlemanager import HandleManager
from mtp.storage import StorageManager, FilesystemStorage
from mtp.object import ObjectInfo, ObjectPropertyCode, ObjectPropertyCodeArray, ObjectPropertyDesc, builddesc
from mtp.partialfile import PartialFile


operations = {}

def operation(f):
    """Add any function with this decorator to operations map.

    The map is used when parsing operation packets, which have
    a string for the operation. Thus, to handle an operation
    packet, simply create a function with the appropriate name
    and add this decorator.
    """
    operations[f.__name__] = f
    return f

def filereceiver(f):
    """Decorator for operations which receive data from the inquirer.

    The data stage must run even if there is an error with the operation.
    """
    def receivefile(self, p):
        try:
            (dest, params) = f(self, p)
        except MTPError as e:
            self.receivefile(p.code, p.tx_id, open('/dev/null', 'wb'))
            raise e
        else:
            self.receivefile(p.code, p.tx_id, dest)
            print(params)
            return params
    # For compatibility with @operation we must mangle the name.
    receivefile.__name__ = f.__name__
    return receivefile

def receiver(f):
    """Decorator for operations which receive data from the inquirer.

    The data stage must run even if there is an error with the operation.
    """
    def receivedata(self, p):
        return f(self, p, self.receivedata(p.code, p.tx_id))
    # For compatibility with @operation we must mangle the name.
    receivedata.__name__ = f.__name__
    return receivedata

def sender(f):
    """Decorator for operations which send data to the inquirer.

    The data stage must run even if there is an error with the operation.
    """
    def senddata(self, p):
        try:
            (data, params) = f(self, p)
        except MTPError as e:
            self.senddata(p.code, p.tx_id, io.BytesIO(b''))
            raise e
        else:
            self.senddata(p.code, p.tx_id, data)
            return params
    # For compatibility with @operation we must mangle the name.
    senddata.__name__ = f.__name__
    return senddata

def session(f):
    """Decorator for operations which require a session to be open.

    Returns a SESSION_NOT_OPEN response if no session is open,
    otherwise it calls the handler.
    """
    def check_session(self, *args):
        if self.session_id is None:
            raise MTPError('SESSION_NOT_OPEN')
        else:
            return f(self, *args)
    # For compatibility with @operation we must mangle the name.
    check_session.__name__ = f.__name__
    return check_session


class MTPResponder(object):

    def __init__(self, outep, inep, intep, loop):
        self.outep = outep
        self.inep = inep
        self.intep = intep
        self.loop = loop
        self.loop.add_reader(self.outep, self.handleOneOperation)
        self.loop.add_reader(self.intep, self.intep.pump)

        self.session_id = None
        self.properties = DeviceProperties(
            ('DEVICE_FRIENDLY_NAME', 'Whizzle'),
            ('SYNCHRONIZATION_PARTNER', '', True),
        )

        self.object_info = None

        self.eventqueue = []
        self.wm = WatchManager()
        self.hm = HandleManager()
        self.sm = StorageManager(self.hm)

        FilesystemStorage('Files', '/tmp/mtp', self.sm, self.hm, self.wm)

        self.loop.add_reader(self.wm, self.wm.dispatch)

    def senddata(self, code, tx_id, f):
        f.seek(0, 2) # move the cursor to the end of the file
        length = f.tell()
        f.seek(0, 0) # move back to the beginning
        mtpdata = MTPData.build(dict(length=length+12, code=code, tx_id=tx_id))
        self.inep.write(mtpdata)
        if length == 0:
            return
        while length >= 512: # TODO: this should be connection max packet size rather than 512
            self.inep.write(f.read(512))
            length -= 512
        if length >= 0: # geq because we need to send null sentinal packet iff len(data) is a multiple of 512
            self.inep.write(f.read(length))


    def receivedata(self, code, tx_id):
        bio = io.BytesIO()
        self.receivefile(code, tx_id, bio)
        data = bytes(bio.getbuffer())
        return data

    def receivefile(self, code, tx_id, f):
        buf = self.outep.read()
        mtpdata = MTPData.parse(buf)
        length = mtpdata.length-12
        if length == 0:
            return
        while length >= 512: # TODO: this should be connection max packet size rather than 512
            buf = self.outep.read()
            f.write(buf)
            if len(buf) != 512:
                raise MTPError('INCOMPLETE_TRANSFER')
            length -= 512
        if length >= 0: # geq because we need to send null sentinal packet iff len(data) is a multiple of 512
            buf = self.outep.read()
            if len(buf) != length:
                raise MTPError('INCOMPLETE_TRANSFER')
            f.write(buf)
        if mtpdata.code != code:
            raise MTPError('INVALID_DATASET')
        if mtpdata.tx_id != tx_id:
            raise MTPError('INVALID_TRANSACTION_ID')

    def respond(self, code, tx_id, p1=None, p2=None, p3=None, p4=None, p5=None):
        args = locals()
        del args['self']
        logger.debug(' '.join(str(x) for x in ('Response:', args['code'], args['p1'], args['p2'], args['p3'], args['p4'], args['p5'])))
        self.inep.write(MTPResponse.build(args))


    @operation
    @sender
    def GET_DEVICE_INFO(self, p):
        data = DeviceInfo.build(dict(
                 device_properties_supported=self.properties.supported(),
                 operations_supported=sorted(operations.keys(), key=lambda o: OperationCode.encoding[o]),
                 events_supported=sorted([
                     'OBJECT_ADDED',
                     'OBJECT_REMOVED',
                     'OBJECT_INFO_CHANGED',
                     'STORE_ADDED',
                     'STORE_REMOVED',
                     'STORAGE_INFO_CHANGED',
                     'STORE_FULL',
                     'DEVICE_INFO_CHANGED',
                     'DEVICE_RESET',
                     'UNREPORTED_STATUS',
                 ], key=lambda e: EventCode.encoding[e])
               ))
        return (io.BytesIO(data), ())

    @operation
    def OPEN_SESSION(self, p):
        if self.session_id is not None:
            raise MTPError('SESSION_ALREADY_OPEN', (self.session_id,))
        else:
            self.session_id = p.p1
        logger.info('Session opened.')
        return (self.session_id,)

    @operation
    @session
    def CLOSE_SESSION(self, p):
        self.session_id = None
        logger.info('Session closed.')
        return ()

    @operation
    @sender
    @session
    def GET_STORAGE_IDS(self, p):
        data = DataType.formats['AUINT32'].build(list(self.sm.ids()))
        return (io.BytesIO(data), ())

    @operation
    @sender
    @session
    def GET_STORAGE_INFO(self, p):
        data = self.sm[p.p1].build()
        return (io.BytesIO(data), ())

    @operation
    @session
    def GET_NUM_OBJECTS(self, p):
        if p.p2 != 0:
            raise MTPError('SPECIFICATION_BY_FORMAT_UNSUPPORTED')
        else:
            num = len(self.sm.handles(p.p1, p.p3))
        return (num, )

    @operation
    @sender
    @session
    def GET_OBJECT_HANDLES(self, p):
        if p.p2 != 0:
            raise MTPError('SPECIFICATION_BY_FORMAT_UNSUPPORTED')
        else:
            data = DataType.formats['AUINT32'].build(list(self.sm.handles(p.p1, p.p3)))

        logger.debug(' '.join(str(x) for x in ('Data:', *DataType.formats['AUINT32'].parse(data))))
        return (io.BytesIO(data), ())

    @operation
    @sender
    @session
    def GET_OBJECT_INFO(self, p):
        data = self.hm[p.p1].build()
        return (io.BytesIO(data), ())

    @operation
    @sender
    @session
    def GET_OBJECT(self, p):
        f = self.hm[p.p1].open(mode='rb')
        return (f, ())

    @operation
    @session
    def DELETE_OBJECT(self, p):
        self.hm[p.p1].delete()
        return ()

    @operation
    @receiver
    @session
    def SEND_OBJECT_INFO(self, p, data):
        if p.p1 == 0:
            if p.p2 != 0:
                logger.warning('SEND_OBJECT_INFO: parent handle specified without storage. Continuing anyway.')
            storage = self.sm.default_store
        else:
            storage = self.sm[p.p1]

        if p.p2 == 0xffffffff:
            parent = storage.root
        elif p.p2 == 0:
            parent = storage.root
        else:
            parent = self.hm[p.p2]
            if parent.storage != storage:
                logger.warning('SEND_OBJECT_INFO: parent handle is in a different storage. Continuing anyway.')
            if not parent.path().is_dir():
                raise MTPError('INVALID_PARENT_OBJECT')

        info = ObjectInfo.parse(data)
        if info.format == 'ASSOCIATION' and info.association_type == 'GENERIC_FOLDER':
            parent.path().mkdir(info.name)
            parent.add_child(parent.path() / info.filename)
        handle = self.hm.reserve_handle()
        self.object_info = (parent, info, handle)
        return ()

    @operation
    @filereceiver
    @session
    def SEND_OBJECT(self, p):
        if self.object_info is None:
            raise MTPError('NO_VALID_OBJECT_INFO')
        (parent, info, handle) = self.object_info
        if info.format == 'ASSOCIATION' and info.association_type == 'GENERIC_FOLDER':
            f = open('/dev/null', 'wb')
        else:
            p = parent.path() / info.filename
            f = p.open('wb')
            parent.add_child(p)
        self.object_info = None
        return (f, ())

    @operation
    @sender
    @session
    def GET_DEVICE_PROP_DESC(self, p):
        data = self.properties[DevicePropertyCode.decoding[p.p1]].builddesc()
        return (io.BytesIO(data), ())

    @operation
    @sender
    @session
    def GET_DEVICE_PROP_VALUE(self, p):
        data = self.properties[DevicePropertyCode.decoding[p.p1]].build()
        return (io.BytesIO(data), ())

    @operation
    @receiver
    @session
    def SET_DEVICE_PROP_VALUE(self, p, data):
        self.properties[DevicePropertyCode.decoding[p.p1]].parse(data)
        return ()

    @operation
    @session
    def RESET_DEVICE_PROP_VALUE(self, p):
        if p.p1 == 0xffffffff:
            self.properties.reset()
        else:
            self.properties[DevicePropertyCode.decoding[p.p1]].reset()
        return ()

    @operation
    @sender
    @session
    def GET_PARTIAL_OBJECT(self, p):
        fp = self.hm[p.p1].partial_file(p.p2, p.p3)
        return (fp, (fp.length,))

    @operation
    @sender
    @session
    def GET_PARTIAL_OBJECT_64(self, p):
        fp = self.hm[p.p1].partial_file(p.p2 | (p.p3<<32), p.p4)
        return (fp, (fp.length,))

    @operation
    @filereceiver
    @session
    def SEND_PARTIAL_OBJECT(self, p):
        fp = self.hm[p.p1].partial_file(p.p2 | (p.p3 << 32), p.p4)
        return (fp, ())

    @operation
    @session
    def TRUNCATE_OBJECT(self, p):
        self.hm[p.p1].truncate(p.p2 | (p.p3 << 32))
        return ()

    @operation
    @session
    def BEGIN_EDIT_OBJECT(self, p):
        return ()

    @operation
    @session
    def END_EDIT_OBJECT(self, p):
        return ()

#    @operation
#    @sender
#    @session
#    def GET_OBJECT_PROPS_SUPPORTED(self, p):
#        logger.warning('format {}'.format(hex(p.p1)))
#        data = ObjectPropertyCodeArray.build(['STORAGE_ID', 'OBJECT_FORMAT', 'PROTECTION_STATUS', 'OBJECT_SIZE', 'OBJECT_FILE_NAME', 'DATE_MODIFIED', 'PARENT_OBJECT', 'NAME'])
#        return (io.BytesIO(data), ())

#    @operation
#    @sender
#    @session
#    def GET_OBJECT_PROP_DESC(self, p):
#        data = builddesc(ObjectPropertyCode.decoding[p.p1])
#        return (io.BytesIO(data), ())

#    @operation
#    @sender
#    @session
#    def GET_OBJECT_PROP_VALUE(self, p):
#        obj = self.hm[p.p1]
#        code = ObjectPropertyCode.decoding[p.p2]
#        if code == 'STORAGE_ID':
#            data = obj.storage.id
#        elif code == 'OBJECT_FORMAT':
#            data = 0x3001 if obj.path().is_dir() else 0x3000
#        elif code == 'PROTECTION_STATUS':
#            data = 0
#        elif code == 'OBJECT_SIZE':
#            data = obj.path().stat().st_size
#        elif code == 'OBJECT_FILE_NAME' or code == 'NAME':
#            data = 'asd'
#        elif code == 'DATE_MODIFIED':
#            data = ''
#        elif code == 'PARENT_OBJECT':
#            data = obj.parent.handle
#        else:
#            raise MTPError(code='INVALID_OBJECT_PROP_CODE')
#        data = ObjectPropertyCode.formats[code].build(data)
#        return (io.BytesIO(data), ())

#    @operation
#    @receiver
#    @session
#    def SET_OBJECT_PROP_VALUE(self, p, value):
#        return ()

#    @operation
#    @sender
#    def GET_OBJECT_PROP_LIST(self, p):
#        data = DataType.formats['AUINT32'].build([])
#        return (io.BytesIO(data), ())

#    @operation
#    @sender
#    @session
#    def GET_OBJECT_REFERENCES(self, p):
#        return (io.BytesIO(b''), ())

#    @operation
#    @receiver
#    @session
#    def SET_OBJECT_REFERENCES(self, p, value):
#        return ()


    def operations(self, code):
        try:
            return operations[code]
        except KeyError:
            raise MTPError('OPERATION_NOT_SUPPORTED')

    def handleOneOperation(self):
        try:
            buf = self.outep.read()
        except IOError as e: # inquirer disconnected?
            logger.error('IOError when reading: %d' % (e.args[0]))
            self.outep.submit()
            return
        # TODO: parser can't handle short packets without p1-p5 args, so extend buffer with zeros.
        buf += b'\x00'*(32-len(buf))
        p = MTPOperation.parse(buf)
        logger.debug(' '.join(str(x) for x in ('Operation:', p.code, hex(p.p1), hex(p.p2), hex(p.p3), hex(p.p4), hex(p.p5))))
        if p.code not in ['SEND_OBJECT']:
            self.object_info = None
        try:
            self.respond('OK', p.tx_id, *self.operations(p.code)(self, p))
        except MTPError as e:
            logger.warning(' '.join(str(x) for x in ('Operation:', p.code, hex(p.p1), hex(p.p2), hex(p.p3), hex(p.p4), hex(p.p5))))
            logger.warning(' '.join(str(x) for x in ('MTPError:', e)))
            self.respond(e.code, p.tx_id, *e.params)
