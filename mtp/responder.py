from __future__ import print_function

import errno
import binascii
import queue

from .packets import parse, MTPResponse
from .constants import *

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
        p = parse(buf)
        print(p.length, p.type, hex(p.code), p.transaction_id)
        self.inep.write(MTPResponse(code=MTP_RESPONSE_OK, transaction_id=p.transaction_id))
