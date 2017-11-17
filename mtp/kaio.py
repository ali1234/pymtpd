import os
import ctypes
from errno import EINTR

import logging
logger = logging.getLogger(__name__)

# from https://github.com/chrisjbillington/inotify_simple/blob/master/inotify_simple/inotify_simple.py

_libc = ctypes.cdll.LoadLibrary('libc.so.6')
_libc.__errno_location.restype = ctypes.POINTER(ctypes.c_int)

def _libc_call(function, *args):
    while True:
        rc = function(*args)
        if rc == -1:
            errno = _libc.__errno_location().contents.value
            if errno  == EINTR:
                continue
            else:
                raise OSError(errno, os.strerror(errno))
        return rc

# from https://stackoverflow.com/questions/3565417/using-python-ctypes-to-call-io-submit-in-linux

def PADDED64(type, name1, name2):
    return [(name1, type), (name2, type)]

def PADDEDptr64(type, name1, name2):
    return [(name1, type)]

def PADDEDul64(name1, name2):
    return [(name1, ctypes.c_ulong)]

class IOVec(ctypes.Structure):
    _fields_ = [("iov_base", ctypes.c_void_p), ("iov_len", ctypes.c_size_t)]

class IOCBDataCommon64(ctypes.Structure):
    _fields_ = PADDEDptr64(ctypes.c_void_p, "buf", "__pad1") + \
        PADDEDul64("nbytes", "__pad2") + \
        [("offset", ctypes.c_longlong), ("__pad3", ctypes.c_longlong), ("flags", ctypes.c_uint), ("resfd", ctypes.c_uint)]

class IOCBDataVector(ctypes.Structure):
    _fields_ = [("vec", ctypes.POINTER(IOVec)), ("nr", ctypes.c_int), ("offset", ctypes.c_longlong)]

class IOCBDataPoll64(ctypes.Structure):
    _fields_ = PADDED64(ctypes.c_int, "events", "__pad1")

class SockAddr(ctypes.Structure):
    _fields_ = [("sa_family", ctypes.c_ushort), ("sa_data", ctypes.c_char * 14)]

class IOCBDataSockAddr(ctypes.Structure):
    _fields_ = [("addr", ctypes.POINTER(SockAddr)), ("len", ctypes.c_int)]

class IOCBDataUnion64(ctypes.Union):
    _fields_ = [("c", IOCBDataCommon64), ("v", IOCBDataVector), ("poll", IOCBDataPoll64), ("saddr", IOCBDataSockAddr)]

class IOCB64(ctypes.Structure):
    _fields_ = PADDEDptr64(ctypes.c_void_p, "data" , "__pad1") + \
        PADDED64(ctypes.c_uint, "key", "__pad2") + \
        [("aio_lio_opcode", ctypes.c_short), ("aio_reqprio", ctypes.c_short), ("aio_fildes", ctypes.c_int), ("u", IOCBDataUnion64)]

class Timespec(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_nsec", ctypes.c_long)]

class IOEvent64(ctypes.Structure):
    _fields_ = PADDEDptr64(ctypes.c_void_p, "data", "__pad1") + \
        PADDEDptr64(ctypes.POINTER(IOCB64), "obj", "__pad2") + \
        PADDEDul64("res", "__pad3") + \
        PADDEDul64("res2", "__pad4")

def io_submit(self, aioContext, aioCommands):
    iocbPtr = ctypes.cast(aioCommands.getIOCBArray(), ctypes.POINTER(self.iocb_t))
    return self.__aio.io_submit(aioContext, aioCommands.size(), ctypes.byref(iocbPtr))

_libaio = ctypes.cdll.LoadLibrary('libaio.so')
#_libaio = ctypes.cdll.LoadLibrary('/home/al/nvidiathing/libfakeaio.so')
_libaio.__errno_location.restype = ctypes.POINTER(ctypes.c_int)

def _libaio_call(function, *args):
    rc = function(*args)
    logger.debug("libaio call: %s(%s) -> %d" % (function.__name__, ' '.join(str(a) for a in args), rc))
    if rc < 0:
        raise OSError(-rc, os.strerror(-rc))
    return rc


class KAIOReader(object):
    def __init__(self, file):
        self.file = file
        self.filefd = file if type(file) == int else file.fileno()
        self.evfd = _libc_call(_libc.eventfd, 0, 0)
        self.__closed = False
        logger.debug('filefd = %d, evfd = %d' % (self.filefd, self.evfd))

        self.buf = ctypes.c_buffer(512)

        # note: io_context_t is "an opaque pointer type" and "can be safely passed by value".
        self.ctx = ctypes.c_void_p(0)

        # int io_setup(unsigned nr_events, io_context_t *ctx_idp);
        _libaio_call(_libaio.io_setup, 1, ctypes.byref(self.ctx))

        # static inline void io_prep_pread(struct iocb *iocb, int fd, void *buf, size_t count, long long offset)
        # {
        #    memset(iocb, 0, sizeof(*iocb));
        #    iocb->aio_fildes = fd;
        #    iocb->aio_lio_opcode = IO_CMD_PREAD;
        #    iocb->aio_reqprio = 0;
        #    iocb->u.c.buf = buf;
        #    iocb->u.c.nbytes = count;
        #    iocb->u.c.offset = offset;
        # }

        self.iocb = IOCB64()
        self.iocb.aio_fildes = self.filefd
        self.iocb.aio_lio_opcode = 0 # IO_CMD_PREAD
        self.iocb.aio_reqprio = 0
        self.iocb.u.c.buf = ctypes.cast(self.buf, ctypes.c_void_p)
        self.iocb.u.c.nbytes = 512
        self.iocb.u.c.offset = 0

        self.iocb.u.c.flags = 1 # IOCB_FLAG_RESFD
        self.iocb.u.c.resfd = self.evfd
        self.iocbptr = ctypes.pointer(self.iocb)

    def fileno(self):
        return self.evfd

    def submit(self):
        # int io_submit(io_context_t ctx_id, long nr, struct iocb **iocbpp);
        _libaio_call(_libaio.io_submit, self.ctx, ctypes.c_long(1), ctypes.byref(self.iocbptr))

    def read(self):
        os.read(self.evfd, 8)
        e = IOEvent64()

        # int io_getevents(io_context_t ctx_id, long min_nr, long nr,
        #                struct io_event *events, struct timespec *timeout);
        ret = _libaio_call(_libaio.io_getevents, self.ctx, ctypes.c_long(1), ctypes.c_long(1), ctypes.byref(e), None)
        if ret == 1 :
            tmp = bytes(self.buf)
        else:
            raise Exception('This should never happen')
        self.submit() # prime a new read operation
        return tmp

    def close(self):
        # python-functionfs likes to call close() twice. This is not a problem
        # for regular fds, but will cause EINVAL with io_destroy().
        if not self.__closed:
            _libaio_call(_libaio.io_destroy, self.ctx)
            os.close(self.evfd)
            self.__closed = True


if __name__ == '__main__':
    f = os.open('/tmp/mtp/foo.txt', os.O_RDWR)
    k = KAIOReader(f)
    while(True):
        print(k.read())