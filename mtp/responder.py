from __future__ import print_function

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

def session(f):
    """Decorator for operations which require a session to be open.

    Returns a SESSION_NOT_OPEN response if no session is open,
    otherwise it calls the handler.
    """
    def check_session(self, p):
        if self.session_id is None:
            self.respond('SESSION_NOT_OPEN', p.tx_id)
        else:
            f(self, p)
    # For compatibility with @operation we must mangle the name.
    check_session.__name__ = f.__name__
    return check_session

class MTPResponder(object):

    def __init__(self, outep, inep, intep):
        self.outep = outep
        self.inep = inep
        self.intep = intep
        self.session_id = None
        self.properties = DeviceProperties()

        self.properties.add('DEVICE_FRIENDLY_NAME', 'Whizzle')
        self.properties.add('SYNCHRONIZATION_PARTNER', '', True)

    def datastage(self, data):
        print(MTPData.parse(data))
#        self.inep.write(data[:12])
#        self.inep.write(data[12:])
        self.inep.write(data)

    def respond(self, code, tx_id, p1=None, p2=None, p3=None, p4=None, p5=None):
        self.inep.write(MTPResponse.build(dict(code=code, tx_id=tx_id, p1=p1, p2=p2, p3=p3, p4=p4, p5=p5)))

    @operation
    def GET_DEVICE_INFO(self, p):
        di = MTPDeviceInfo.build(dict(
                 device_properties_supported=list(self.properties.props.keys()),
                 operations_supported=list(operations.keys()),
             ))
        data = MTPData.build(dict(code=p.code, tx_id=p.tx_id, data=di))
        self.datastage(data)
        self.respond('OK', p.tx_id)

    @operation
    def OPEN_SESSION(self, p):
        if self.session_id is not None:
            self.respond('SESSION_ALREADY_OPEN', p.tx_id, self.session_id)
        else:
            self.session_id = p.p1
            self.respond('OK', p.tx_id)

    @operation
    @session
    def CLOSE_SESSION(self, p):
        self.session_id = None
        self.respond('OK', p.tx_id)

    @operation
    @session
    def GET_DEVICE_PROP_VALUE(self, p):
        di = self.properties[DevicePropertyCode.decoding[p.p1]].build()
        data = MTPData.build(dict(code=p.code, tx_id=p.tx_id, data=di))
        self.datastage(data)
        self.respond('OK', p.tx_id)


    def handleOneOperation(self):
        buf = bytearray(512)
        self.outep.readinto(buf)
        p = MTPCommand.parse(buf)
        print(p)
        try:
            #getattr(self, p.code)(p)
            f = operations[p.code]
        except KeyError:
            self.inep.write(MTPResponse.build(dict(code='OPERATION_NOT_SUPPORTED', tx_id=p.tx_id)))
            return
        else:
            f(self, p)
