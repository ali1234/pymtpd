from construct import *

import mtp.constants

FormatType = Enum(Int16ul, **dict(mtp.constants.format_types))
ObjectPropertyCode = Enum(Int16ul, **dict(mtp.constants.object_property_codes))
