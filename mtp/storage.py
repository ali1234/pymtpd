from construct import *

import mtp.constants


StorageType = Enum(Int16ul, dict(mtp.constants.storage_types))
StorageAccess = Enum(Int16ul, dict(mtp.constants.storage_accesss))
AssociationType = Enum(Int16ul, dict(mtp.constants.association_types))