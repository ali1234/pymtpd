import io

import logging
logger = logging.getLogger(__name__)

from mtp.exceptions import MTPError
from mtp.device import DeviceInfo, DeviceProperties, DevicePropertyCode
from mtp.packets import MTPOperation, MTPResponse, DataFormats, OperationCode, EventCode
from mtp.watchmanager import WatchManager
from mtp.handlemanager import HandleManager
from mtp.storage import StorageManager, FilesystemStorage
from mtp.object import ObjectInfo, ObjectPropertyCode, ObjectPropertyCodeArray, ObjectPropertyDesc, builddesc
from mtp.registry import Registry

class MTPResponder(object):
    operations = Registry()

    def __init__(self, outep, inep, intep, loop, args):
        self.outep = outep
        self.inep = inep
        self.intep = intep
        self.loop = loop
        self.loop.add_reader(self.outep, self.handleOneOperation)
        self.loop.add_reader(self.intep, self.intep.pump)

        self.session_id = None
        self.properties = DeviceProperties(
            ('DEVICE_FRIENDLY_NAME', args.name),
            ('SYNCHRONIZATION_PARTNER', '', True),
        )

        self.object_info = None

        self.eventqueue = []
        self.wm = WatchManager()
        self.hm = HandleManager()
        self.sm = StorageManager(self.hm)

        for s in args.storage:
            FilesystemStorage(s[0], s[1], self.sm, self.hm, self.wm)

        self.loop.add_reader(self.wm, self.wm.dispatch)

    @operations.sender
    def GET_DEVICE_INFO(self, p):
        data = DeviceInfo.build(dict(
                 device_properties_supported=self.properties.supported(),
                 operations_supported=sorted(self.operations.keys(), key=lambda o: OperationCode.encmapping[o]),
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
                 ], key=lambda e: EventCode.encmapping[e])
               ))
        return (io.BytesIO(data), ())

    @operations
    def OPEN_SESSION(self, p):
        if self.session_id is not None:
            raise MTPError('SESSION_ALREADY_OPEN', (self.session_id,))
        else:
            self.session_id = p.p1
        logger.info('Session opened.')
        return (self.session_id,)

    @operations.session
    def CLOSE_SESSION(self, p):
        self.session_id = None
        logger.info('Session closed.')
        return ()

    @operations.sender
    def GET_STORAGE_IDS(self, p):
        data = DataFormats['AUINT32'].build(list(self.sm.ids()))
        return (io.BytesIO(data), ())

    @operations.sender
    def GET_STORAGE_INFO(self, p):
        data = self.sm[p.p1].build()
        return (io.BytesIO(data), ())

    @operations.session
    def GET_NUM_OBJECTS(self, p):
        if p.p2 != 0:
            raise MTPError('SPECIFICATION_BY_FORMAT_UNSUPPORTED')
        else:
            num = len(self.sm.handles(p.p1, p.p3))
        return (num, )

    @operations.sender
    def GET_OBJECT_HANDLES(self, p):
        if p.p2 != 0:
            raise MTPError('SPECIFICATION_BY_FORMAT_UNSUPPORTED')
        else:
            data = DataFormats['AUINT32'].build(list(self.sm.handles(p.p1, p.p3)))

        logger.debug(' '.join(str(x) for x in ('Data:', *DataFormats['AUINT32'].parse(data))))
        return (io.BytesIO(data), ())

    @operations.sender
    def GET_OBJECT_INFO(self, p):
        data = self.hm[p.p1].build()
        return (io.BytesIO(data), ())

    @operations.sender
    def GET_OBJECT(self, p):
        f = self.hm[p.p1].open(mode='rb')
        return (f, ())

    @operations.session
    def DELETE_OBJECT(self, p):
        self.hm[p.p1].delete()
        return ()

    @operations.receiver
    def SEND_OBJECT_INFO(self, p, data):
        if p.p1 == 0:
            if p.p2 != 0:
                logger.warning('SEND_OBJECT_INFO: parent handle specified without storage. Continuing anyway.')
            storage = self.sm.default_store
        else:
            storage = self.sm[p.p1]

        if p.p2 == 0xffffffff or p.p2 == 0:
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
            handle = parent.add_child(parent.path() / info.filename)
        elif info.compressed_size == 0:
            f = (parent.path() / info.filename).open('wb')
            f.close()
            handle = parent.add_child(parent.path() / info.filename)
        else:
            handle = self.hm.reserve_handle()
        self.object_info = (parent, info, handle)
        return (parent.storage.id, parent.handle_as_parent(), handle)

    @operations.filereceiver
    def SEND_OBJECT(self, p):
        if self.object_info is None:
            raise MTPError('NO_VALID_OBJECT_INFO')
        (parent, info, handle) = self.object_info
        if (info.format == 'ASSOCIATION' and info.association_type == 'GENERIC_FOLDER') or info.compressed_size == 0:
            f = open('/dev/null', 'wb')
        else:
            p = parent.path() / info.filename
            f = p.open('wb')
            parent.add_child(p, handle)
        self.object_info = None
        return (f, ())

    @operations.sender
    def GET_DEVICE_PROP_DESC(self, p):
        data = self.properties[DevicePropertyCode.decmapping[p.p1]].builddesc()
        return (io.BytesIO(data), ())

    @operations.sender
    def GET_DEVICE_PROP_VALUE(self, p):
        data = self.properties[DevicePropertyCode.decmapping[p.p1]].build()
        return (io.BytesIO(data), ())

    @operations.receiver
    def SET_DEVICE_PROP_VALUE(self, p, data):
        self.properties[DevicePropertyCode.decmapping[p.p1]].parse(data)
        return ()

    @operations.session
    def RESET_DEVICE_PROP_VALUE(self, p):
        if p.p1 == 0xffffffff:
            self.properties.reset()
        else:
            self.properties[DevicePropertyCode.decmapping[p.p1]].reset()
        return ()

    @operations.sender
    def GET_PARTIAL_OBJECT(self, p):
        fp = self.hm[p.p1].partial_file(p.p2, p.p3)
        return (fp, (fp.length,))

    @operations.sender
    def GET_PARTIAL_OBJECT_64(self, p):
        fp = self.hm[p.p1].partial_file(p.p2 | (p.p3<<32), p.p4)
        return (fp, (fp.length,))

    @operations.filereceiver
    def SEND_PARTIAL_OBJECT(self, p):
        fp = self.hm[p.p1].partial_file(p.p2 | (p.p3 << 32), p.p4)
        return (fp, ())

    @operations.session
    def TRUNCATE_OBJECT(self, p):
        self.hm[p.p1].truncate(p.p2 | (p.p3 << 32))
        return ()

    @operations.session
    def BEGIN_EDIT_OBJECT(self, p):
        return ()

    @operations.session
    def END_EDIT_OBJECT(self, p):
        return ()

#    @operations.sender
#    def GET_OBJECT_PROPS_SUPPORTED(self, p):
#        logger.warning('format {}'.format(hex(p.p1)))
#        data = ObjectPropertyCodeArray.build(['STORAGE_ID', 'OBJECT_FORMAT', 'PROTECTION_STATUS', 'OBJECT_SIZE', 'OBJECT_FILE_NAME', 'DATE_MODIFIED', 'PARENT_OBJECT', 'NAME'])
#        return (io.BytesIO(data), ())

#    @operations.sender
#    def GET_OBJECT_PROP_DESC(self, p):
#        data = builddesc(ObjectPropertyCode.decmapping[p.p1])
#        return (io.BytesIO(data), ())

#    @operations.sender
#    def GET_OBJECT_PROP_VALUE(self, p):
#        obj = self.hm[p.p1]
#        code = ObjectPropertyCode.decmapping[p.p2]
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
#        data = ObjectPropertyFormats[code].build(data)
#        return (io.BytesIO(data), ())

#    @operations.receiver
#    def SET_OBJECT_PROP_VALUE(self, p, value):
#        return ()

#    @operations.sender
#    def GET_OBJECT_PROP_LIST(self, p):
#        data = DataFormats['AUINT32'].build([])
#        return (io.BytesIO(data), ())

#    @operations.sender
#    def GET_OBJECT_REFERENCES(self, p):
#        return (io.BytesIO(b''), ())

#    @operations.receiver
#    def SET_OBJECT_REFERENCES(self, p, value):
#        return ()

    def respond(self, code, tx_id, p1=0, p2=0, p3=0, p4=0, p5=0):
        args = locals()
        del args['self']
        logger.debug(' '.join(str(x) for x in ('Response:', args['code'], hex(args['p1']), hex(args['p2']), hex(args['p3']), hex(args['p4']), hex(args['p5']))))
        self.inep.write(MTPResponse.build(args))

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
            self.respond('OK', p.tx_id, *self.operations[p.code](self, p))
        except MTPError as e:
            logger.warning(' '.join(str(x) for x in ('Operation:', p.code, hex(p.p1), hex(p.p2), hex(p.p3), hex(p.p4), hex(p.p5))))
            logger.warning(' '.join(str(x) for x in ('MTPError:', e)))
            self.respond(e.code, p.tx_id, *e.params)
