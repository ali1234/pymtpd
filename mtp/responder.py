from __future__ import print_function

from mtp.deviceproperties import DeviceProperties
from .packets import MTPCommand, MTPResponse, MTPData
from .types import *

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

    def __init__(self, outep, inep, intep):
        self.outep = outep
        self.inep = inep
        self.intep = intep
        self.session_id = None
        self.properties = DeviceProperties(
            ('DEVICE_FRIENDLY_NAME', 'Whizzle'),
            ('SYNCHRONIZATION_PARTNER', '', True),
        )

    def senddata(self, code, tx_id, data):
        # TODO: handle transfers bigger than one packet
        mtpdata = MTPData.build(dict(code=code, tx_id=tx_id, data=data))
        self.inep.write(mtpdata)

    def receivedata(self, code, tx_id):
        # TODO: handle transfers bigger than one packet
        buf = bytearray(512)
        self.outep.readinto(buf)
        mtpdata = MTPData.parse(buf)
        #TODO: check code
        if mtpdata.tx_id != tx_id:
            raise MTPError('INVALID_TRANSACTION_ID')
        return mtpdata.data

    def respond(self, code, tx_id, p1=None, p2=None, p3=None, p4=None, p5=None):
        args = locals()
        del args['self']
        self.inep.write(MTPResponse.build(args))


    @operation
    @sender
    def GET_DEVICE_INFO(self, p):
        data = MTPDeviceInfo.build(dict(
                 device_properties_supported=list(self.properties.keys()),
                 operations_supported=list(operations.keys()),
               ))
        return (data, ())

    @operation
    def OPEN_SESSION(self, p):
        if self.session_id is not None:
            raise MTPError('SESSION_ALREADY_OPEN', (self.session_id,))
        else:
            self.session_id = p.p1
        return (self.session_id,)

    @operation
    @session
    def CLOSE_SESSION(self, p):
        self.session_id = None
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


    def operations(self, code):
        try:
            return operations[code]
        except KeyError:
            raise MTPError('OPERATION_NOT_SUPPORTED')

    def handleOneOperation(self):

        buf = bytearray(512)
        self.outep.readinto(buf)
        p = MTPCommand.parse(buf)

        try:
            self.respond('OK', p.tx_id, *self.operations(p.code)(self, p))
        except MTPError as e:
            print('MTPError:', e)
            print('Operation', p)
            self.respond(e.code, p.tx_id, *e.params)
