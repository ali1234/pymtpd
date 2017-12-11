from construct import *

import mtp.constants
from mtp.exceptions import MTPError


ContainerType = Enum(Int16ul, **dict(mtp.constants.container_types))
OperationCode = Enum(Int16ul, **dict(mtp.constants.operation_codes))
ResponseCode = Enum(Int16ul, **dict(mtp.constants.response_codes))
EventCode = Enum(Int16ul, **dict(mtp.constants.event_codes))

DataType = Enum(Int16ul, **{x[0]: x[1] for x in mtp.constants.data_types})
DataFormats = {x[0]: x[2] for x in mtp.constants.data_types}


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
    'length' / Int32ul,
    'type' / Const(ContainerType, 'DATA'),
    'code' / OperationCode,
    'tx_id' / Int32ul,
)

MTPEvent = Struct(
    'length' / Const(Int32ul, 24),
    'type' / Const(ContainerType, 'EVENT'),
    'code' / EventCode,
    'tx_id' / Default(Int32ul, 0),
    'p1' / Default(Int32ul, 0),
    'p2' / Default(Int32ul, 0),
    'p3' / Default(Int32ul, 0),
)

# functions for dealing with data stage packets.

def indata(inep, code, tx_id, f):
    f.seek(0, 2)  # move the cursor to the end of the file
    length = f.tell()
    f.seek(0, 0)  # move back to the beginning
    mtpdata = MTPData.build(dict(length=length + 12, code=code, tx_id=tx_id))
    inep.write(mtpdata)
    if length == 0:
        return
    while length >= inep.maxpkt:  # TODO: this should be connection max packet size rather than 512
        inep.write(f.read(inep.maxpkt))
        length -= inep.maxpkt
    if length >= 0:  # geq because we need to send null sentinal packet iff len(data) is a multiple of 512
        inep.write(f.read(length))


def outdata(outep, code, tx_id, f):
    buf = outep.read()
    mtpdata = MTPData.parse(buf)
    length = mtpdata.length - 12
    if length == 0:
        return
    while length >= outep.maxpkt:  # TODO: this should be connection max packet size rather than 512
        buf = outep.read()
        f.write(buf)
        if len(buf) != outep.maxpkt:
            raise MTPError('INCOMPLETE_TRANSFER')
        length -= outep.maxpkt
    if length >= 0:  # geq because we need to send null sentinal packet iff len(data) is a multiple of 512
        buf = outep.read()
        if len(buf) != length:
            raise MTPError('INCOMPLETE_TRANSFER')
        f.write(buf)
    if mtpdata.code != code:
        raise MTPError('INVALID_DATASET')
    if mtpdata.tx_id != tx_id:
        raise MTPError('INVALID_TRANSACTION_ID')


if __name__ == '__main__':
    from binascii import hexlify
    b = MTPData.build(dict(code='GET_DEVICE_PROP_VALUE', tx_id=5, data=b'12345'))
    p = MTPData.parse(b)
    print(p)
    print(hexlify(b))
