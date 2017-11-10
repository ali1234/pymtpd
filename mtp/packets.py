from construct import *
from construct.lib import *

from .constants import *


mtp_command = Struct(
    'length' / Int32ul,
    'type' / Const(container_type, 'COMMAND'),
    'code' / operation_code,
    'tx_id' / Int32ul,
    'p1' / Default(Int32ul, 0),
    'p2' / Default(Int32ul, 0),
    'p3' / Default(Int32ul, 0),
    'p4' / Default(Int32ul, 0),
    'p5' / Default(Int32ul, 0),
)

mtp_response = Struct(
    'length' / Const(Int32ul, 32),
    'type' / Const(container_type, 'RESPONSE'),
    'code' / response_code,
    'tx_id' / Int32ul,
    'p1' / Default(Int32ul, 0),
    'p2' / Default(Int32ul, 0),
    'p3' / Default(Int32ul, 0),
    'p4' / Default(Int32ul, 0),
    'p5' / Default(Int32ul, 0),
)

mtp_data = Struct(
    'length' / Rebuild(Int32ul, len_(this.data)),
    'type' / Const(container_type, 'DATA'),
    'code' / Default(Int32ul, 0),
    'tx_id', Int32ul,
    'data' / Byte[this.count],
)

mtp_event = Struct(
    'length' / Const(Int32ul, 24),
    'type' / Const(container_type, 'EVENT'),
    'code' / event_code,
    'tx_id' / Int32ul,
    'parameters' / Default(Array(3, Int32ul), [0,0,0]),
)
