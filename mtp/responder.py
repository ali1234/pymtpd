from __future__ import print_function

import errno
import binascii

from .packets import MTPHeader
from .constants import *

class MTPResponder(object):

    def __init__(self, outep, inep, intep):
        self.outep = outep
        self.inep = inep
        self.intep = intep

    def run(self):
        buf = bytearray(512)
        self.outep.readinto(buf)
        h = MTPHeader.from_buffer(buf)
        print(h.length, h.type, hex(h.code), h.transaction_id)
        if h.type == MTP_CONTAINER_TYPE_COMMAND:
            if h.code == MTP_OPERATION_OPEN_SESSION:
                print('host wants to open session')
                self.inep.write(MTPHeader(length=12, type=MTP_CONTAINER_TYPE_RESPONSE, code=MTP_RESPONSE_OK, transaction_id=h.transaction_id))
            elif h.code == MTP_OPERATION_GET_DEVICE_INFO:
                print('host asked for device info')
                self.inep.write(MTPHeader(length=12, type=MTP_CONTAINER_TYPE_RESPONSE, code=MTP_RESPONSE_OK, transaction_id=h.transaction_id))

