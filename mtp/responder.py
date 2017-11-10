from __future__ import print_function

import errno
import binascii
import queue

from .packets import mtp_command, mtp_response

class MTPResponder(object):

    def __init__(self, outep, inep, intep):
        self.outep = outep
        self.inep = inep
        self.intep = intep
        self.responses = queue.Queue()
        self.events = queue.Queue()

    def handleOneOperation(self):
        buf = bytearray(512)
        self.outep.readinto(buf)
        p = mtp_command.parse(buf)
        print(p)
        r = mtp_response.build(dict(code='OK', tx_id=p.tx_id))
        print(mtp_response.parse(r))
        self.inep.write(r)
