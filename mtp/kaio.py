import os
import ctypes
import struct

import logging
logger = logging.getLogger(__name__)

from libaio import eventfd
from libaio.libaio import io_setup, io_prep_pread, io_prep_pwrite, io_submit, io_getevents, io_destroy
from libaio.libaio import io_context_t, iocb, io_event
from libaio.libaio import IOCB_FLAG_RESFD

class KAIOFile(object):


    def __init__(self, file, nr_events=1):
        self.file = file
        self.filefd = file if type(file) == int else file.fileno()
        self.evfd = eventfd(0, 0)
        self.closed = False
        self.ctx = io_context_t()
        io_setup(nr_events, ctypes.byref(self.ctx))

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
        super().__init__(file, 1)
        self.iocb = iocb()
        self.buf = ctypes.c_buffer(512)
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
        if ret != 1 :
            raise Exception('This should never happen')
        tmp = bytearray(e.res)
        tmp[:] = bytes(self.buf[:e.res])
        self.submit() # prime a new read operation
        return tmp


class KAIOWriter(KAIOFile):
    """Queues writes inside the kernel."""

    def __init__(self, file):
        super().__init__(file, 128)
        logger.debug('Created KAIOWriter: filefd = %d, evfd = %d' % (self.filefd, self.evfd))

    def write(self, buf):
        iocb_ = iocb()
        io_prep_pwrite(iocb_, self.filefd, ctypes.cast(buf, ctypes.c_void_p), len(buf), 0)
        iocb_.u.c.flags |= IOCB_FLAG_RESFD
        iocb_.u.c.resfd = self.evfd
        iocbptr = ctypes.pointer(iocb_)
        result = io_submit(self.ctx, 1, ctypes.byref(iocbptr))
        logger.warning('event written')
        # TODO: What happens when buf, iocb_, iocbptr go out of scope?

    def pump(self):
        res = os.read(self.evfd, 8)
        (n_e,) = struct.unpack('Q', res)
        e = (io_event*n_e)()
        ret = io_getevents(self.ctx, n_e, n_e, e, None)
        logger.warning('pumped %d of %d events' % (ret, n_e))
        for i in range(ret):
            logger.warning(' event %d - %d' % (i, e[i].res))
            # TODO: Free buf, iocb_, iocbptr here?




if __name__ == '__main__':
    f = os.open('/tmp/mtp/foo.txt', os.O_RDWR)
    k = KAIOReader(f)
    k.submit()
    while(True):
        print(k.read())