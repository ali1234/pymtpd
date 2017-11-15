from construct import *

import mtp.constants


ContainerType = Enum(Int16ul, **dict(mtp.constants.container_types))
OperationCode = Enum(Int16ul, **dict(mtp.constants.operation_codes))
ResponseCode = Enum(Int16ul, **dict(mtp.constants.response_codes))
EventCode = Enum(Int16ul, **dict(mtp.constants.event_codes))

DataType = Enum(Int16ul, **{x[0]: x[1] for x in mtp.constants.data_types})
DataType.formats = {x[0]: x[2] for x in mtp.constants.data_types}


MTPOperation = Struct(
    'length' / Int32ul,
    'type' / Const(ContainerType, 'OPERATION'),
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
    b = MTPData.build(dict(code='GET_DEVICE_PROP_VALUE', tx_id=5, data=b'12345'))
    p = MTPData.parse(b)
    print(p)
    print(hexlify(b))
