from construct import *

import mtp.constants


StorageType = Enum(Int16ul, dict(mtp.constants.storage_types))
StorageFileSystems = Enum(Int16ul, dict(mtp.constants.storage_file_systems))
StorageAccess = Enum(Int16ul, dict(mtp.constants.storage_accesss))
AssociationType = Enum(Int16ul, dict(mtp.constants.association_types))

StorageInfo = Struct(
    'storage_type' / Default(StorageType, 'FIXED_RAM'),
    'filesystem_type' / Default(StorageFileSystems, 'HIERARCHICAL'),
    'access_capability' / Default(StorageAccess, 'READ_WRITE'),
    'max_capacity' / Int64ul,
    'free_space' / Int64ul,
    'free_space_in_objects' / Default(Int32ul, 0xffffffff),
    'storage_description' / Default(MTPString, u''),
    'volume_identifier' / Default(MTPString, u''),
)