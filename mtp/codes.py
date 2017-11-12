from construct import *

import mtp.constants


DataType = Enum(Int16ul, {x[0]: x[1] for x in mtp.constants.data_types})
DataType.formats = {x[0]: x[2] for x in mtp.constants.data_types}

FormatType = Enum(Int16ul, dict(mtp.constants.format_types))

ObjectPropertyCode = Enum(Int16ul, dict(mtp.constants.object_property_codes))

StorageType = Enum(Int16ul, dict(mtp.constants.storage_types))

StorageAccess = Enum(Int16ul, dict(mtp.constants.storage_accesss))

AssociationType = Enum(Int16ul, dict(mtp.constants.association_types))









