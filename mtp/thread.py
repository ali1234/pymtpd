from __future__ import print_function

import threading
import binascii

from .packets import MTPHeader
from .constants import *

class MTPThread(threading.Thread):
    daemon = True

    def __init__(self, outep, inep, intep, **kw):
        super(MTPThread, self).__init__(**kw)
        self.outep = outep
        self.inep = inep
        self.intep = intep
        self.echo_buf = bytearray(512)
        self.__run_lock = run_lock = threading.Lock()
        run_lock.acquire()
        super(MTPThread, self).start()

    def start(self):
        self.__run_lock.release()

    def run(self):
        echo_buf = self.echo_buf
        run_lock = self.__run_lock
        while True:
            run_lock.acquire()
            print(self.name, 'start')
            while True:
                try:
                    self.outep.readinto(echo_buf)
                    h = MTPHeader.from_buffer(echo_buf)
                    print(h.length, h.type, hex(h.code), h.transaction_id)
                    if h.type == MTP_CONTAINER_TYPE_COMMAND:
                        if h.code == MTP_OPERATION_OPEN_SESSION:
                            print('host wants to open session')
                            self.inep.write(MTPHeader(length=12, type=MTP_CONTAINER_TYPE_RESPONSE, code=MTP_RESPONSE_OK, transaction_id=h.transaction_id))
                        elif h.code == MTP_OPERATION_GET_DEVICE_INFO:
                            print('host asked for device info')
                            self.inep.write(MTPHeader(length=12, type=MTP_CONTAINER_TYPE_RESPONSE, code=MTP_RESPONSE_OK, transaction_id=h.transaction_id))
                except IOError as exc:
                    if exc.errno == errno.ESHUTDOWN:
                        break
                    if exc.errno not in (errno.EINTR, errno.EAGAIN):
                        raise
            print(self.name, 'exit')
            run_lock.acquire(False)

