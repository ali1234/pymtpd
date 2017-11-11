from __future__ import print_function

import errno
import binascii
import queue

from .packets import mtp_command, mtp_response, mtp_data
from .deviceinfo import mtp_device_info

operations = {}

def operation(f):
    operations[f.__name__] = f
    return f

# decorator for operations which require a session to be open
def session(f):
    def check_session(self, p):
        if self.session_id is None:
            self.inep.write(mtp_response.build(dict(code='SESSION_NOT_OPEN', tx_id=p.tx_id)))
        else:
            f(self, p)
    # in order for the operations map to work,
    # we have to fix the name of the decorated function
    check_session.__name__ = f.__name__
    return check_session

class MTPResponder(object):

    def __init__(self, outep, inep, intep):
        self.outep = outep
        self.inep = inep
        self.intep = intep
        self.responses = queue.Queue()
        self.events = queue.Queue()
        self.session_id = None


    def datastage(self, data):
        print(mtp_data.parse(data))
#        self.inep.write(data[:12])
#        self.inep.write(data[12:])
        self.inep.write(data)

    @operation
    def GET_DEVICE_INFO(self, p):
        di = mtp_device_info.build(dict(operations_supported=list(operations.keys())))
        data = mtp_data.build(dict(code=p.code, tx_id=p.tx_id, data=di))
        self.datastage(data)
        self.inep.write(mtp_response.build(dict(code='OK', tx_id=p.tx_id)))

    @operation
    def OPEN_SESSION(self, p):
        if self.session_id is not None:
            self.inep.write(mtp_response.build(dict(code='SESSION_ALREADY_OPEN', tx_id=p.tx_id, p1=self.session_id)))
        else:
            self.session_id = p.p1
            self.inep.write(mtp_response.build(dict(code='OK', tx_id=p.tx_id)))

    @operation
    @session
    def CLOSE_SESSION(self, p):
        self.session_id = None
        self.inep.write(mtp_response.build(dict(code='OK', tx_id=p.tx_id)))


    def handleOneOperation(self):
        buf = bytearray(512)
        self.outep.readinto(buf)
        p = mtp_command.parse(buf)
        print(p)
        try:
            #getattr(self, p.code)(p)
            operations[p.code](self, p)
        except KeyError:
            self.inep.write(mtp_response.build(dict(code='OPERATION_NOT_SUPPORTED', tx_id=p.tx_id)))
