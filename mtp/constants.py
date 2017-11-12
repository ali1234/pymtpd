# Copyright (C) 2010 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from construct import *

from mtp.adapters import MTPString

VERSION = 100

# MTP Container Types
container_types = [
    ('UNDEFINED',   0),
    ('OPERATION',     1),
    ('DATA',        2),
    ('RESPONSE',    3),
    ('EVENT',       4),
]

# MTP Data Types
data_types = [
    ('UNDEFINED',     0x0000, Pass),
    ('INT8',          0x0001, Byte),
    ('UINT8',         0x0002, Byte),
    ('INT16',         0x0003, Int16sl),
    ('UINT16',        0x0004, Int16ul),
    ('INT32',         0x0005, Int32sl),
    ('UINT32',        0x0006, Int32ul),
    ('INT64',         0x0007, Int64sl),
    ('UINT64',        0x0008, Int64ul),
#    ('INT128':        0x0009, Int128sl),
#    ('UINT128':       0x000A, Int128ul),
    ('AINT8',         0x4001, PrefixedArray(Int32ul, Byte)),
    ('AUINT8',        0x4002, PrefixedArray(Int32ul, Byte)),
    ('AINT16',        0x4003, PrefixedArray(Int32ul, Int16sl)),
    ('AUINT16',       0x4004, PrefixedArray(Int32ul, Int16ul)),
    ('AINT32',        0x4005, PrefixedArray(Int32ul, Int32sl)),
    ('AUINT32',       0x4006, PrefixedArray(Int32ul, Int32ul)),
    ('AINT64',        0x4007, PrefixedArray(Int32ul, Int64sl)),
    ('AUINT64',       0x4008, PrefixedArray(Int32ul, Int64ul)),
#    ('AINT128',       0x4009, PrefixedArray(Int32ul, Int128sl)),
#    ('AUINT128',      0x400A, PrefixedArray(Int32ul, Int128ul)),
    ('STR',           0xFFFF, MTPString),
]

# MTP Format Codes
format_types = [
    ('UNDEFINED',                           0x3000),   # Undefined object
    ('ASSOCIATION',                         0x3001),   # Association (for example, a folder)
    ('SCRIPT',                              0x3002),   # Device model-specific script
    ('EXECUTABLE',                          0x3003),   # Device model-specific binary executable
    ('TEXT',                                0x3004),   # Text file
    ('HTML',                                0x3005),   # Hypertext Markup Language file (text)
    ('DPOF',                                0x3006),   # Digital Print Order Format file (text)
    ('AIFF',                                0x3007),   # Audio clip
    ('WAV',                                 0x3008),   # Audio clip
    ('MP3',                                 0x3009),   # Audio clip
    ('AVI',                                 0x300A),   # Video clip
    ('MPEG',                                0x300B),   # Video clip
    ('ASF',                                 0x300C),   # Microsoft Advanced Streaming Format (video)
    ('DEFINED',                             0x3800),   # Unknown image object
    ('EXIF_JPEG',                           0x3801),   # Exchangeable File Format, JEIDA standard
    ('TIFF_EP',                             0x3802),   # Tag Image File Format for Electronic Photography
    ('FLASHPIX',                            0x3803),   # Structured Storage Image Format
    ('BMP',                                 0x3804),   # Microsoft Windows Bitmap file
    ('CIFF',                                0x3805),   # Canon Camera Image File Format
    ('GIF',                                 0x3807),   # Graphics Interchange Format
    ('JFIF',                                0x3808),   # JPEG File Interchange Format
    ('CD',                                  0x3809),   # PhotoCD Image Pac
    ('PICT',                                0x380A),   # Quickdraw Image Format
    ('PNG',                                 0x380B),   # Portable Network Graphics
    ('TIFF',                                0x380D),   # Tag Image File Format
    ('TIFF_IT',                             0x380E),   # Tag Image File Format for Information Technology (graphic arts)
    ('JP2',                                 0x380F),   # JPEG2000 Baseline File Format
    ('JPX',                                 0x3810),   # JPEG2000 Extended File Format
    ('UNDEFINED_FIRMWARE',                  0xB802),
    ('WINDOWS_IMAGE_FORMAT',                0xB881),
    ('UNDEFINED_AUDIO',                     0xB900),
    ('WMA',                                 0xB901),
    ('OGG',                                 0xB902),
    ('AAC',                                 0xB903),
    ('AUDIBLE',                             0xB904),
    ('FLAC',                                0xB906),
    ('UNDEFINED_VIDEO',                     0xB980),
    ('WMV',                                 0xB981),
    ('MP4_CONTAINER',                       0xB982),  # ISO 14496-1
    ('MP2',                                 0xB983),
    ('THREEGP_CONTAINER',                   0xB984),  # 3GPP file format. Details: http://www.3gpp.org/ftp/Specs/html-info/26244.htm
    ('UNDEFINED_COLLECTION',                0xBA00),
    ('ABSTRACT_MULTIMEDIA_ALBUM',           0xBA01),
    ('ABSTRACT_IMAGE_ALBUM',                0xBA02),
    ('ABSTRACT_AUDIO_ALBUM',                0xBA03),
    ('ABSTRACT_VIDEO_ALBUM',                0xBA04),
    ('ABSTRACT_AV_PLAYLIST',                0xBA05),
    ('ABSTRACT_CONTACT_GROUP',              0xBA06),
    ('ABSTRACT_MESSAGE_FOLDER',             0xBA07),
    ('ABSTRACT_CHAPTERED_PRODUCTION',       0xBA08),
    ('ABSTRACT_AUDIO_PLAYLIST',             0xBA09),
    ('ABSTRACT_VIDEO_PLAYLIST',             0xBA0A),
    ('ABSTRACT_MEDIACAST',                  0xBA0B), # For use with mediacasts; references multimedia enclosures of RSS feeds or episodic content
    ('WPL_PLAYLIST',                        0xBA10),
    ('M3U_PLAYLIST',                        0xBA11),
    ('MPL_PLAYLIST',                        0xBA12),
    ('ASX_PLAYLIST',                        0xBA13),
    ('PLS_PLAYLIST',                        0xBA14),
    ('UNDEFINED_DOCUMENT',                  0xBA80),
    ('ABSTRACT_DOCUMENT',                   0xBA81),
    ('XML_DOCUMENT',                        0xBA82),
    ('MS_WORD_DOCUMENT',                    0xBA83),
    ('MHT_COMPILED_HTML_DOCUMENT',          0xBA84),
    ('MS_EXCEL_SPREADSHEET',                0xBA85),
    ('MS_POWERPOINT_PRESENTATION',          0xBA86),
    ('UNDEFINED_MESSAGE',                   0xBB00),
    ('ABSTRACT_MESSSAGE',                   0xBB01),
    ('UNDEFINED_CONTACT',                   0xBB80),
    ('ABSTRACT_CONTACT',                    0xBB81),
    ('VCARD_2',                             0xBB82),
]

# MTP Object Property Codes
object_property_codes = [
    ('STORAGE_ID',                            0xDC01),
    ('OBJECT_FORMAT',                         0xDC02),
    ('PROTECTION_STATUS',                     0xDC03),
    ('OBJECT_SIZE',                           0xDC04),
    ('ASSOCIATION_TYPE',                      0xDC05),
    ('ASSOCIATION_DESC',                      0xDC06),
    ('OBJECT_FILE_NAME',                      0xDC07),
    ('DATE_CREATED',                          0xDC08),
    ('DATE_MODIFIED',                         0xDC09),
    ('KEYWORDS',                              0xDC0A),
    ('PARENT_OBJECT',                         0xDC0B),
    ('ALLOWED_FOLDER_CONTENTS',               0xDC0C),
    ('HIDDEN',                                0xDC0D),
    ('SYSTEM_OBJECT',                         0xDC0E),
    ('PERSISTENT_UID',                        0xDC41),
    ('SYNC_ID',                               0xDC42),
    ('PROPERTY_BAG',                          0xDC43),
    ('NAME',                                  0xDC44),
    ('CREATED_BY',                            0xDC45),
    ('ARTIST',                                0xDC46),
    ('DATE_AUTHORED',                         0xDC47),
    ('DESCRIPTION',                           0xDC48),
    ('URL_REFERENCE',                         0xDC49),
    ('LANGUAGE_LOCALE',                       0xDC4A),
    ('COPYRIGHT_INFORMATION',                 0xDC4B),
    ('SOURCE',                                0xDC4C),
    ('ORIGIN_LOCATION',                       0xDC4D),
    ('DATE_ADDED',                            0xDC4E),
    ('NON_CONSUMABLE',                        0xDC4F),
    ('CORRUPT_UNPLAYABLE',                    0xDC50),
    ('PRODUCER_SERIAL_NUMBER',                0xDC51),
    ('REPRESENTATIVE_SAMPLE_FORMAT',          0xDC81),
    ('REPRESENTATIVE_SAMPLE_SIZE',            0xDC82),
    ('REPRESENTATIVE_SAMPLE_HEIGHT',          0xDC83),
    ('REPRESENTATIVE_SAMPLE_WIDTH',           0xDC84),
    ('REPRESENTATIVE_SAMPLE_DURATION',        0xDC85),
    ('REPRESENTATIVE_SAMPLE_DATA',            0xDC86),
    ('WIDTH',                                 0xDC87),
    ('HEIGHT',                                0xDC88),
    ('DURATION',                              0xDC89),
    ('RATING',                                0xDC8A),
    ('TRACK',                                 0xDC8B),
    ('GENRE',                                 0xDC8C),
    ('CREDITS',                               0xDC8D),
    ('LYRICS',                                0xDC8E),
    ('SUBSCRIPTION_CONTENT_ID',               0xDC8F),
    ('PRODUCED_BY',                           0xDC90),
    ('USE_COUNT',                             0xDC91),
    ('SKIP_COUNT',                            0xDC92),
    ('LAST_ACCESSED',                         0xDC93),
    ('PARENTAL_RATING',                       0xDC94),
    ('META_GENRE',                            0xDC95),
    ('COMPOSER',                              0xDC96),
    ('EFFECTIVE_RATING',                      0xDC97),
    ('SUBTITLE',                              0xDC98),
    ('ORIGINAL_RELEASE_DATE',                 0xDC99),
    ('ALBUM_NAME',                            0xDC9A),
    ('ALBUM_ARTIST',                          0xDC9B),
    ('MOOD',                                  0xDC9C),
    ('DRM_STATUS',                            0xDC9D),
    ('SUB_DESCRIPTION',                       0xDC9E),
    ('IS_CROPPED',                            0xDCD1),
    ('IS_COLOUR_CORRECTED',                   0xDCD2),
    ('IMAGE_BIT_DEPTH',                       0xDCD3),
    ('F_NUMBER',                              0xDCD4),
    ('EXPOSURE_TIME',                         0xDCD5),
    ('EXPOSURE_INDEX',                        0xDCD6),
    ('TOTAL_BITRATE',                         0xDE91),
    ('BITRATE_TYPE',                          0xDE92),
    ('SAMPLE_RATE',                           0xDE93),
    ('NUMBER_OF_CHANNELS',                    0xDE94),
    ('AUDIO_BIT_DEPTH',                       0xDE95),
    ('SCAN_TYPE',                             0xDE97),
    ('AUDIO_WAVE_CODEC',                      0xDE99),
    ('AUDIO_BITRATE',                         0xDE9A),
    ('VIDEO_FOURCC_CODEC',                    0xDE9B),
    ('VIDEO_BITRATE',                         0xDE9C),
    ('FRAMES_PER_THOUSAND_SECONDS',           0xDE9D),
    ('KEYFRAME_DISTANCE',                     0xDE9E),
    ('BUFFER_SIZE',                           0xDE9F),
    ('ENCODING_QUALITY',                      0xDEA0),
    ('ENCODING_PROFILE',                      0xDEA1),
    ('DISPLAY_NAME',                          0xDCE0),
    ('BODY_TEXT',                             0xDCE1),
    ('SUBJECT',                               0xDCE2),
    ('PRIORITY',                              0xDCE3),
    ('GIVEN_NAME',                            0xDD00),
    ('MIDDLE_NAMES',                          0xDD01),
    ('FAMILY_NAME',                           0xDD02),
    ('PREFIX',                                0xDD03),
    ('SUFFIX',                                0xDD04),
    ('PHONETIC_GIVEN_NAME',                   0xDD05),
    ('PHONETIC_FAMILY_NAME',                  0xDD06),
    ('EMAIL_PRIMARY',                         0xDD07),
    ('EMAIL_PERSONAL_1',                      0xDD08),
    ('EMAIL_PERSONAL_2',                      0xDD09),
    ('EMAIL_BUSINESS_1',                      0xDD0A),
    ('EMAIL_BUSINESS_2',                      0xDD0B),
    ('EMAIL_OTHERS',                          0xDD0C),
    ('PHONE_NUMBER_PRIMARY',                  0xDD0D),
    ('PHONE_NUMBER_PERSONAL',                 0xDD0E),
    ('PHONE_NUMBER_PERSONAL_2',               0xDD0F),
    ('PHONE_NUMBER_BUSINESS',                 0xDD10),
    ('PHONE_NUMBER_BUSINESS_2',               0xDD11),
    ('PHONE_NUMBER_MOBILE',                   0xDD12),
    ('PHONE_NUMBER_MOBILE_2',                 0xDD13),
    ('FAX_NUMBER_PRIMARY',                    0xDD14),
    ('FAX_NUMBER_PERSONAL',                   0xDD15),
    ('FAX_NUMBER_BUSINESS',                   0xDD16),
    ('PAGER_NUMBER',                          0xDD17),
    ('PHONE_NUMBER_OTHERS',                   0xDD18),
    ('PRIMARY_WEB_ADDRESS',                   0xDD19),
    ('PERSONAL_WEB_ADDRESS',                  0xDD1A),
    ('BUSINESS_WEB_ADDRESS',                  0xDD1B),
    ('INSTANT_MESSANGER_ADDRESS',             0xDD1C),
    ('INSTANT_MESSANGER_ADDRESS_2',           0xDD1D),
    ('INSTANT_MESSANGER_ADDRESS_3',           0xDD1E),
    ('POSTAL_ADDRESS_PERSONAL_FULL',          0xDD1F),
    ('POSTAL_ADDRESS_PERSONAL_LINE_1',        0xDD20),
    ('POSTAL_ADDRESS_PERSONAL_LINE_2',        0xDD21),
    ('POSTAL_ADDRESS_PERSONAL_CITY',          0xDD22),
    ('POSTAL_ADDRESS_PERSONAL_REGION',        0xDD23),
    ('POSTAL_ADDRESS_PERSONAL_POSTAL_CODE',   0xDD24),
    ('POSTAL_ADDRESS_PERSONAL_COUNTRY',       0xDD25),
    ('POSTAL_ADDRESS_BUSINESS_FULL',          0xDD26),
    ('POSTAL_ADDRESS_BUSINESS_LINE_1',        0xDD27),
    ('POSTAL_ADDRESS_BUSINESS_LINE_2',        0xDD28),
    ('POSTAL_ADDRESS_BUSINESS_CITY',          0xDD29),
    ('POSTAL_ADDRESS_BUSINESS_REGION',        0xDD2A),
    ('POSTAL_ADDRESS_BUSINESS_POSTAL_CODE',   0xDD2B),
    ('POSTAL_ADDRESS_BUSINESS_COUNTRY',       0xDD2C),
    ('POSTAL_ADDRESS_OTHER_FULL',             0xDD2D),
    ('POSTAL_ADDRESS_OTHER_LINE_1',           0xDD2E),
    ('POSTAL_ADDRESS_OTHER_LINE_2',           0xDD2F),
    ('POSTAL_ADDRESS_OTHER_CITY',             0xDD30),
    ('POSTAL_ADDRESS_OTHER_REGION',           0xDD31),
    ('POSTAL_ADDRESS_OTHER_POSTAL_CODE',      0xDD32),
    ('POSTAL_ADDRESS_OTHER_COUNTRY',          0xDD33),
    ('ORGANIZATION_NAME',                     0xDD34),
    ('PHONETIC_ORGANIZATION_NAME',            0xDD35),
    ('ROLE',                                  0xDD36),
    ('BIRTHDATE',                             0xDD37),
    ('MESSAGE_TO',                            0xDD40),
    ('MESSAGE_CC',                            0xDD41),
    ('MESSAGE_BCC',                           0xDD42),
    ('MESSAGE_READ',                          0xDD43),
    ('MESSAGE_RECEIVED_TIME',                 0xDD44),
    ('MESSAGE_SENDER',                        0xDD45),
    ('ACTIVITY_BEGIN_TIME',                   0xDD50),
    ('ACTIVITY_END_TIME',                     0xDD51),
    ('ACTIVITY_LOCATION',                     0xDD52),
    ('ACTIVITY_REQUIRED_ATTENDEES',           0xDD54),
    ('ACTIVITY_OPTIONAL_ATTENDEES',           0xDD55),
    ('ACTIVITY_RESOURCES',                    0xDD56),
    ('ACTIVITY_ACCEPTED',                     0xDD57),
    ('ACTIVITY_TENTATIVE',                    0xDD58),
    ('ACTIVITY_DECLINED',                     0xDD59),
    ('ACTIVITY_REMAINDER_TIME',               0xDD5A),
    ('ACTIVITY_OWNER',                        0xDD5B),
    ('ACTIVITY_STATUS',                       0xDD5C),
    ('OWNER',                                 0xDD5D),
    ('EDITOR',                                0xDD5E),
    ('WEBMASTER',                             0xDD5F),
    ('URL_SOURCE',                            0xDD60),
    ('URL_DESTINATION',                       0xDD61),
    ('TIME_BOOKMARK',                         0xDD62),
    ('OBJECT_BOOKMARK',                       0xDD63),
    ('BYTE_BOOKMARK',                         0xDD64),
    ('LAST_BUILD_DATE',                       0xDD70),
    ('TIME_TO_LIVE',                          0xDD71),
    ('MEDIA_GUID',                            0xDD72),
]

# MTP Device Property Codes
device_property_codes = [
    ('UNDEFINED',                      0x5000, 'UNDEFINED'),
    ('BATTERY_LEVEL',                  0x5001, 'UINT8'),
    ('FUNCTIONAL_MODE',                0x5002, 'UINT16'),
    ('IMAGE_SIZE',                     0x5003, 'STR'),
    ('COMPRESSION_SETTING',            0x5004, 'UINT8'),
    ('WHITE_BALANCE',                  0x5005, 'UINT16'),
    ('RGB_GAIN',                       0x5006, 'STR'),
    ('F_NUMBER',                       0x5007, 'UINT16'),
    ('FOCAL_LENGTH',                   0x5008, 'UINT32'),
    ('FOCUS_DISTANCE',                 0x5009, 'UINT16'),
    ('FOCUS_MODE',                     0x500A, 'UINT16'),
    ('EXPOSURE_METERING_MODE',         0x500B, 'UINT16'),
    ('FLASH_MODE',                     0x500C, 'UINT16'),
    ('EXPOSURE_TIME',                  0x500D, 'UINT32'),
    ('EXPOSURE_PROGRAM_MODE',          0x500E, 'UINT16'),
    ('EXPOSURE_INDEX',                 0x500F, 'UINT16'),
    ('EXPOSURE_BIAS_COMPENSATION',     0x5010, 'INT16'),
    ('DATETIME',                       0x5011, 'STR'),
    ('CAPTURE_DELAY',                  0x5012, 'UINT32'),
    ('STILL_CAPTURE_MODE',             0x5013, 'UINT16'),
    ('CONTRAST',                       0x5014, 'UINT8'),
    ('SHARPNESS',                      0x5015, 'UINT8'),
    ('DIGITAL_ZOOM',                   0x5016, 'UINT8'),
    ('EFFECT_MODE',                    0x5017, 'UINT16'),
    ('BURST_NUMBER',                   0x5018, 'UINT16'),
    ('BURST_INTERVAL',                 0x5019, 'UINT16'),
    ('TIMELAPSE_NUMBER',               0x501A, 'UINT16'),
    ('TIMELAPSE_INTERVAL',             0x501B, 'UINT32'),
    ('FOCUS_METERING_MODE',            0x501C, 'UINT32'),
    ('UPLOAD_URL',                     0x501D, 'STR'),
    ('ARTIST',                         0x501E, 'STR'),
    ('COPYRIGHT_INFO',                 0x501F, 'STR'),
    ('SYNCHRONIZATION_PARTNER',        0xD401, 'STR'),
    ('DEVICE_FRIENDLY_NAME',           0xD402, 'STR'),
    ('VOLUME',                         0xD403, 'UINT32'),
    ('SUPPORTED_FORMATS_ORDERED',      0xD404, 'UINT8'),
    ('DEVICE_ICON',                    0xD405, 'AUINT8'),
    ('PLAYBACK_RATE',                  0xD410, 'INT32'),
    ('PLAYBACK_OBJECT',                0xD411, 'UINT32'),
    ('PLAYBACK_CONTAINER_INDEX',       0xD412, 'UINT32'),
    ('PLAYBACK_POSITION',              0xD413, 'UINT32'),
    ('SESSION_INITIATOR_VERSION_INFO', 0xD406, 'STR'),
    ('PERCEIVED_DEVICE_TYPE',          0xD407, 'UINT32'),
]

# MTP Operation Codes
operation_codes = [
    ('GET_DEVICE_INFO',                      0x1001),
    ('OPEN_SESSION',                         0x1002),
    ('CLOSE_SESSION',                        0x1003),
    ('GET_STORAGE_IDS',                      0x1004),
    ('GET_STORAGE_INFO',                     0x1005),
    ('GET_NUM_OBJECTS',                      0x1006),
    ('GET_OBJECT_HANDLES',                   0x1007),
    ('GET_OBJECT_INFO',                      0x1008),
    ('GET_OBJECT',                           0x1009),
    ('GET_THUMB',                            0x100A),
    ('DELETE_OBJECT',                        0x100B),
    ('SEND_OBJECT_INFO',                     0x100C),
    ('SEND_OBJECT',                          0x100D),
    ('INITIATE_CAPTURE',                     0x100E),
    ('FORMAT_STORE',                         0x100F),
    ('RESET_DEVICE',                         0x1010),
    ('SELF_TEST',                            0x1011),
    ('SET_OBJECT_PROTECTION',                0x1012),
    ('POWER_DOWN',                           0x1013),
    ('GET_DEVICE_PROP_DESC',                 0x1014),
    ('GET_DEVICE_PROP_VALUE',                0x1015),
    ('SET_DEVICE_PROP_VALUE',                0x1016),
    ('RESET_DEVICE_PROP_VALUE',              0x1017),
    ('TERMINATE_OPEN_CAPTURE',               0x1018),
    ('MOVE_OBJECT',                          0x1019),
    ('COPY_OBJECT',                          0x101A),
    ('GET_PARTIAL_OBJECT',                   0x101B),
    ('INITIATE_OPEN_CAPTURE',                0x101C),
    ('GET_OBJECT_PROPS_SUPPORTED',           0x9801),
    ('GET_OBJECT_PROP_DESC',                 0x9802),
    ('GET_OBJECT_PROP_VALUE',                0x9803),
    ('SET_OBJECT_PROP_VALUE',                0x9804),
    ('GET_OBJECT_PROP_LIST',                 0x9805),
    ('SET_OBJECT_PROP_LIST',                 0x9806),
    ('GET_INTERDEPENDENT_PROP_DESC',         0x9807),
    ('SEND_OBJECT_PROP_LIST',                0x9808),
    ('GET_OBJECT_REFERENCES',                0x9810),
    ('SET_OBJECT_REFERENCES',                0x9811),
    ('SKIP',                                 0x9820),

# Android extensions for direct file IO

# Same as GetPartialObject, but with 64 bit offset
    ('GET_PARTIAL_OBJECT_64',                0x95C1),
# Same as GetPartialObject64, but copying host to device
    ('SEND_PARTIAL_OBJECT',                  0x95C2),
# Truncates file to 64 bit length
    ('TRUNCATE_OBJECT',                      0x95C3),
# Must be called before using SendPartialObject and TruncateObject
    ('BEGIN_EDIT_OBJECT',                    0x95C4),
# Called to commit changes made by SendPartialObject and TruncateObject
    ('END_EDIT_OBJECT',                      0x95C5),
]

# MTP Response Codes
response_codes = [
    ('UNDEFINED',                                 0x2000),
    ('OK',                                        0x2001),
    ('GENERAL_ERROR',                             0x2002),
    ('SESSION_NOT_OPEN',                          0x2003),
    ('INVALID_TRANSACTION_ID',                    0x2004),
    ('OPERATION_NOT_SUPPORTED',                   0x2005),
    ('PARAMETER_NOT_SUPPORTED',                   0x2006),
    ('INCOMPLETE_TRANSFER',                       0x2007),
    ('INVALID_STORAGE_ID',                        0x2008),
    ('INVALID_OBJECT_HANDLE',                     0x2009),
    ('DEVICE_PROP_NOT_SUPPORTED',                 0x200A),
    ('INVALID_OBJECT_FORMAT_CODE',                0x200B),
    ('STORAGE_FULL',                              0x200C),
    ('OBJECT_WRITE_PROTECTED',                    0x200D),
    ('STORE_READ_ONLY',                           0x200E),
    ('ACCESS_DENIED',                             0x200F),
    ('NO_THUMBNAIL_PRESENT',                      0x2010),
    ('SELF_TEST_FAILED',                          0x2011),
    ('PARTIAL_DELETION',                          0x2012),
    ('STORE_NOT_AVAILABLE',                       0x2013),
    ('SPECIFICATION_BY_FORMAT_UNSUPPORTED',       0x2014),
    ('NO_VALID_OBJECT_INFO',                      0x2015),
    ('INVALID_CODE_FORMAT',                       0x2016),
    ('UNKNOWN_VENDOR_CODE',                       0x2017),
    ('CAPTURE_ALREADY_TERMINATED',                0x2018),
    ('DEVICE_BUSY',                               0x2019),
    ('INVALID_PARENT_OBJECT',                     0x201A),
    ('INVALID_DEVICE_PROP_FORMAT',                0x201B),
    ('INVALID_DEVICE_PROP_VALUE',                 0x201C),
    ('INVALID_PARAMETER',                         0x201D),
    ('SESSION_ALREADY_OPEN',                      0x201E),
    ('TRANSACTION_CANCELLED',                     0x201F),
    ('SPECIFICATION_OF_DESTINATION_UNSUPPORTED',  0x2020),
    ('INVALID_OBJECT_PROP_CODE',                  0xA801),
    ('INVALID_OBJECT_PROP_FORMAT',                0xA802),
    ('INVALID_OBJECT_PROP_VALUE',                 0xA803),
    ('INVALID_OBJECT_REFERENCE',                  0xA804),
    ('GROUP_NOT_SUPPORTED',                       0xA805),
    ('INVALID_DATASET',                           0xA806),
    ('SPECIFICATION_BY_GROUP_UNSUPPORTED',        0xA807),
    ('SPECIFICATION_BY_DEPTH_UNSUPPORTED',        0xA808),
    ('OBJECT_TOO_LARGE',                          0xA809),
    ('OBJECT_PROP_NOT_SUPPORTED',                 0xA80A),
]

# MTP Event Codes
event_codes = [
    ('UNDEFINED',                        0x4000),
    ('CANCEL_TRANSACTION',               0x4001),
    ('OBJECT_ADDED',                     0x4002),
    ('OBJECT_REMOVED',                   0x4003),
    ('STORE_ADDED',                      0x4004),
    ('STORE_REMOVED',                    0x4005),
    ('DEVICE_PROP_CHANGED',              0x4006),
    ('OBJECT_INFO_CHANGED',              0x4007),
    ('DEVICE_INFO_CHANGED',              0x4008),
    ('REQUEST_OBJECT_TRANSFER',          0x4009),
    ('STORE_FULL',                       0x400A),
    ('DEVICE_RESET',                     0x400B),
    ('STORAGE_INFO_CHANGED',             0x400C),
    ('CAPTURE_COMPLETE',                 0x400D),
    ('UNREPORTED_STATUS',                0x400E),
    ('OBJECT_PROP_CHANGED',              0xC801),
    ('OBJECT_PROP_DESC_CHANGED',         0xC802),
    ('OBJECT_REFERENCES_CHANGED',        0xC803),
]

#, Storage Type
storage_types = [
    ('FIXED_ROM',                      0x0001),
    ('REMOVABLE_ROM',                  0x0002),
    ('FIXED_RAM',                      0x0003),
    ('REMOVABLE_RAM',                  0x0004),
]

# Storage File System
storage_file_systems = [
    ('FLAT',                0x0001),
    ('HIERARCHICAL',        0x0002),
    ('DCF',                 0x0003),
]

# Storage Access Capability
storage_accesss = [
    ('READ_WRITE',                     0x0000),
    ('READ_ONLY_WITHOUT_DELETE',       0x0001),
    ('READ_ONLY_WITH_DELETE',          0x0002),
]

# Association Type
association_types = [
    ('UNDEFINED',             0x0000),
    ('GENERIC_FOLDER',        0x0001),
]

