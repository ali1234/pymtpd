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
from mtp.object import ObjectInfo


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
            self.senddata(p.code, p.tx_id, b'')
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
        self.wm = WatchManager(self.sendevents)
        self.hm = HandleManager(self.queueevent)
        self.sm = StorageManager(self.hm)

        FilesystemStorage('Files', '/tmp/mtp', self.sm, self.hm, self.wm)

        self.loop.add_reader(self.wm, self.wm.dispatch)

    def queueevent(self, **kwargs):
        if self.session_id is not None:
            self.eventqueue.append(kwargs)

    def sendevents(self):
        if len(self.eventqueue) > 10:
            self.intep.write(MTPEvent.build(dict(code='UNREPORTED_STATUS')))
            logger.warning('Event spam detected, dropped queue, sent UNREPORTED_STATUS instead.')
        else:
            for kwargs in self.eventqueue:
                self.intep.write(MTPEvent.build(kwargs))
                logger.debug('Send event %s' % (str(kwargs)))
        self.eventqueue = []

    def senddata(self, code, tx_id, data):
        length = len(data)
        bio = io.BytesIO(data)
        mtpdata = MTPData.build(dict(length=length+12, code=code, tx_id=tx_id, data=data))
        self.inep.write(mtpdata)
        if length == 0:
            return
        while length >= 512: # TODO: this should be connection max packet size rather than 512
            self.inep.write(bio.read(512))
            length -= 512
        if length >= 0: # geq because we need to send null sentinal packet iff len(data) is a multiple of 512
            self.inep.write(bio.read(length))

    def receivedata(self, code, tx_id):
        buf = self.outep.read()
        mtpdata = MTPData.parse(buf)
        length = mtpdata.length-12
        if length == 0:
            return b''
        bio = io.BytesIO()
        while length >= 512: # TODO: this should be connection max packet size rather than 512
            bio.write(self.outep.read(512))
            length -= 512
        if length >= 0: # geq because we need to handle null sentinal packet iff len(data) is a multiple of 512
            bio.write(self.outep.read(length))
        data = bytes(bio.getbuffer())
        if mtpdata.code != code:
            raise MTPError('INVALID_DATASET')
        if mtpdata.tx_id != tx_id:
            raise MTPError('INVALID_TRANSACTION_ID')
        if len(data) != mtpdata.length:
            raise MTPError('INCOMPLETE_TRANSFER')
        return data

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
        return (data, ())

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
        return(data, ())

    @operation
    @sender
    @session
    def GET_STORAGE_INFO(self, p):
        data = self.sm[p.p1].build()
        return (data, ())

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
        return (data, ())

    @operation
    @sender
    @session
    def GET_OBJECT_INFO(self, p):
        data = self.hm[p.p1].build()
        return (data, ())

    @operation
    @sender
    @session
    def GET_OBJECT(self, p):
        f = self.hm[p.p1].open(mode='rb')
        return (f.read(), ())

    @operation
    @session
    def DELETE_OBJECT(self, p):
        obj = self.hm[p.p1]
        obj.unwatch()
        obj.unregister_children()
        obj.parent.predelete(obj.name)
        if obj.path().is_dir():
            shutil.rmtree(str(obj.path()))
        else:
            obj.path().unlink()
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
        handle = self.hm.reserve_handle()
        self.object_info = (parent, info, handle)

    @operation
    @receiver
    @session
    def SEND_OBJECT(self, p, data):
        if self.object_info is None:
            raise MTPError('NO_VALID_OBJECT_INFO')
        (parent, info, handle) = self.object_info
        parent.precreate(info.name, handle)
        p = parent.path() / info.name
        f = p.open('w')
        f.write(data)
        return ()

    @operation
    @sender
    @session
    def GET_DEVICE_PROP_DESC(self, p):
        data = self.properties[DevicePropertyCode.decoding[p.p1]].builddesc()
        return (data, ())

    @operation
    @sender
    @session
    def GET_DEVICE_PROP_VALUE(self, p):
        data = self.properties[DevicePropertyCode.decoding[p.p1]].build()
        return (data, ())

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
        f = self.hm[p.p1].open(mode='rb')
        f.seek(p.p2, 0)
        data = f.read(p.p3)
        return (data, (len(data),))


    def operations(self, code):
        try:
            return operations[code]
        except KeyError:
            raise MTPError('OPERATION_NOT_SUPPORTED')

    def handleOneOperation(self):
        try:
            buf = self.outep.read()
        except IOError: # inquirer disconnected
            self.session_id = None
            return
        # TODO: parser can't handle short packets without p1-p5 args, so extend buffer with zeros.
        buf += b'\x00'*(32-len(buf))
        p = MTPOperation.parse(buf)
        logger.debug(' '.join(str(x) for x in ('Operation:', p.code, hex(p.p1), hex(p.p2), hex(p.p3), hex(p.p4), hex(p.p5))))

        try:
            self.respond('OK', p.tx_id, *self.operations(p.code)(self, p))
        except MTPError as e:
            logger.warning(' '.join(str(x) for x in ('Operation:', p.code, hex(p.p1), hex(p.p2), hex(p.p3), hex(p.p4), hex(p.p5))))
            logger.warning(' '.join(str(x) for x in ('MTPError:', e)))
            self.respond(e.code, p.tx_id, *e.params)
