import ctypes

u8 = ctypes.c_ubyte
assert ctypes.sizeof(u8) == 1
le16 = ctypes.c_ushort
assert ctypes.sizeof(le16) == 2
le32 = ctypes.c_uint
assert ctypes.sizeof(le32) == 4

from constants import *

class MTPHeader(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('length', le32),
        ('type', le16),
        ('code', le16),
        ('transaction_id', le32),
    ]

