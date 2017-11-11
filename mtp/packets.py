from construct import *
from construct.lib import *

from .types import *

MTPCommand = Struct(
    'length' / Int32ul,
    'type' / Const(ContainerType, 'COMMAND'),
    'code' / OperationCode,
    'tx_id' / Int32ul,
    'p1' / Default(Int32ul, 0),
    'p2' / Default(Int32ul, 0),
    'p3' / Default(Int32ul, 0),
    'p4' / Default(Int32ul, 0),
    'p5' / Default(Int32ul, 0),
)

MTPResponse = Struct(
    'length' / Const(Int32ul, 32),
    'type' / Const(ContainerType, 'RESPONSE'),
    'code' / ResponseCode,
    'tx_id' / Int32ul,
    'p1' / Default(Int32ul, 0),
    'p2' / Default(Int32ul, 0),
    'p3' / Default(Int32ul, 0),
    'p4' / Default(Int32ul, 0),
    'p5' / Default(Int32ul, 0),
)

MTPData = Struct(
    'length' / Rebuild(Int32ul, 12+len_(this.data)),
    'type' / Const(ContainerType, 'DATA'),
    'code' / OperationCode,
    'tx_id' / Int32ul,
    'data' / GreedyBytes,
)

MTPEvent = Struct(
    'length' / Const(Int32ul, 24),
    'type' / Const(ContainerType, 'EVENT'),
    'code' / EventCode,
    'tx_id' / Int32ul,
    'p1' / Default(Int32ul, 0),
    'p2' / Default(Int32ul, 0),
    'p3' / Default(Int32ul, 0),
)

if __name__ == '__main__':
    from binascii import hexlify
    b = MTPData.build(dict(data=b'12345', tx_id=1))
    p = MTPData.parse(b)
    print(p)
    print(hexlify(b))
