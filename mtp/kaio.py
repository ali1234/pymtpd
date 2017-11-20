import os
import ctypes

import logging
logger = logging.getLogger(__name__)

from libaio import eventfd
from libaio.libaio import io_setup, io_prep_pread, io_submit, io_getevents, io_destroy
from libaio.libaio import io_context_t, iocb, io_event
from libaio.libaio import IOCB_FLAG_RESFD

class KAIOFile(object):


    def __init__(self, file):
        self.file = file
        self.filefd = file if type(file) == int else file.fileno()
        self.evfd = eventfd(0, 0)
        self.closed = False
        self.buf = ctypes.c_buffer(512)

        self.ctx = io_context_t()

    def fileno(self):
        return self.evfd

    def close(self):
        # python-functionfs likes to call close() twice. This is not a problem
        # for regular fds, but will cause EINVAL with io_destroy().
        if not self.closed:
            io_destroy(self.ctx)
            os.close(self.evfd)
            self.closed = True


class KAIOReader(KAIOFile):

    """KAIOReader: Wrap a file in Linux Kernel AIO.

    Endpoint files appear like regular files to select() and epoll().
    That means select() will return the fd immediately, and epoll()
    will completely refuse to operate on them.

    This effectively means that you cannot know if read() will block
    before calling it. Instead, the Linux Kernel AIO API must be used,
    via ctypes wrapper to libaio.

    The way KAIOReader works is you give it a fd or a file-like object
    that implements fileno(). It then sets up the eventfd and AIO context.
    KAIOReader.fileno() returns the fd of the eventfd, which will
    become readable when an IO operation submitted by io_submit has
    completed. KAIOReader.read() returns the read buffer.

    This means that from the outside, KAIOReader behaves pretty much
    identical to an endpoint file, except that select() and epoll()
    work on it.

    There are a few gotchas:

    1. KAIOReader.submit() must be called manually the first time.
       io_submit must not be called until after the gadget is bound,
       otherwise it will block forever. But the underlying file must
       be opened before the gadget is bound, so we can't do both at
       the same time.

    2. readinto() etc are not supported, only read().
    """

    def __init__(self, file):
        super().__init__(file)

        io_setup(1, ctypes.byref(self.ctx))

        self.iocb = iocb()
        io_prep_pread(self.iocb, self.filefd, ctypes.cast(self.buf, ctypes.c_void_p), 512, 0)
        self.iocb.u.c.flags |= IOCB_FLAG_RESFD
        self.iocb.u.c.resfd = self.evfd
        self.iocbptr = ctypes.pointer(self.iocb)

        logger.debug('Created KAIOReader: filefd = %d, evfd = %d' % (self.filefd, self.evfd))




    def submit(self):
        io_submit(self.ctx, 1, ctypes.byref(self.iocbptr))

    def read(self):
        os.read(self.evfd, 8)
        e = io_event()

        ret = io_getevents(self.ctx, 1, 1, ctypes.byref(e), None)
        if ret == 1 :
            tmp = bytes(self.buf[:e.res])
        else:
            raise Exception('This should never happen')
        self.submit() # prime a new read operation
        return tmp



if __name__ == '__main__':
    f = os.open('/tmp/mtp/foo.txt', os.O_RDWR)
    k = KAIOReader(f)
    k.submit()
    while(True):
        print(k.read())