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


MTP_STANDARD_VERSION =           100

# Container Types
MTP_CONTAINER_TYPE_UNDEFINED =   0
MTP_CONTAINER_TYPE_COMMAND =     1
MTP_CONTAINER_TYPE_DATA =        2
MTP_CONTAINER_TYPE_RESPONSE =    3
MTP_CONTAINER_TYPE_EVENT =       4

# Container Offsets
MTP_CONTAINER_LENGTH_OFFSET =            0
MTP_CONTAINER_TYPE_OFFSET =              4
MTP_CONTAINER_CODE_OFFSET =              6
MTP_CONTAINER_TRANSACTION_ID_OFFSET =    8
MTP_CONTAINER_PARAMETER_OFFSET =         12
MTP_CONTAINER_HEADER_SIZE =              12

# MTP Data Types
MTP_TYPE_UNDEFINED =     0x0000          # Undefined
MTP_TYPE_INT8 =          0x0001          # Signed 8-bit integer
MTP_TYPE_UINT8 =         0x0002          # Unsigned 8-bit integer
MTP_TYPE_INT16 =         0x0003          # Signed 16-bit integer
MTP_TYPE_UINT16 =        0x0004          # Unsigned 16-bit integer
MTP_TYPE_INT32 =         0x0005          # Signed 32-bit integer
MTP_TYPE_UINT32 =        0x0006          # Unsigned 32-bit integer
MTP_TYPE_INT64 =         0x0007          # Signed 64-bit integer
MTP_TYPE_UINT64 =        0x0008          # Unsigned 64-bit integer
MTP_TYPE_INT128 =        0x0009          # Signed 128-bit integer
MTP_TYPE_UINT128 =       0x000A          # Unsigned 128-bit integer
MTP_TYPE_AINT8 =         0x4001          # Array of signed 8-bit integers
MTP_TYPE_AUINT8 =        0x4002          # Array of unsigned 8-bit integers
MTP_TYPE_AINT16 =        0x4003          # Array of signed 16-bit integers
MTP_TYPE_AUINT16 =       0x4004          # Array of unsigned 16-bit integers
MTP_TYPE_AINT32 =        0x4005          # Array of signed 32-bit integers
MTP_TYPE_AUINT32 =       0x4006          # Array of unsigned 32-bit integers
MTP_TYPE_AINT64 =        0x4007          # Array of signed 64-bit integers
MTP_TYPE_AUINT64 =       0x4008          # Array of unsigned 64-bit integers
MTP_TYPE_AINT128 =       0x4009          # Array of signed 128-bit integers
MTP_TYPE_AUINT128 =      0x400A          # Array of unsigned 128-bit integers
MTP_TYPE_STR =           0xFFFF          # Variable-length Unicode string

# MTP Format Codes
MTP_FORMAT_UNDEFINED =                           0x3000   # Undefined object
MTP_FORMAT_ASSOCIATION =                         0x3001   # Association (for example, a folder)
MTP_FORMAT_SCRIPT =                              0x3002   # Device model-specific script
MTP_FORMAT_EXECUTABLE =                          0x3003   # Device model-specific binary executable
MTP_FORMAT_TEXT =                                0x3004   # Text file
MTP_FORMAT_HTML =                                0x3005   # Hypertext Markup Language file (text)
MTP_FORMAT_DPOF =                                0x3006   # Digital Print Order Format file (text)
MTP_FORMAT_AIFF =                                0x3007   # Audio clip
MTP_FORMAT_WAV =                                 0x3008   # Audio clip
MTP_FORMAT_MP3 =                                 0x3009   # Audio clip
MTP_FORMAT_AVI =                                 0x300A   # Video clip
MTP_FORMAT_MPEG =                                0x300B   # Video clip
MTP_FORMAT_ASF =                                 0x300C   # Microsoft Advanced Streaming Format (video)
MTP_FORMAT_DEFINED =                             0x3800   # Unknown image object
MTP_FORMAT_EXIF_JPEG =                           0x3801   # Exchangeable File Format, JEIDA standard
MTP_FORMAT_TIFF_EP =                             0x3802   # Tag Image File Format for Electronic Photography
MTP_FORMAT_FLASHPIX =                            0x3803   # Structured Storage Image Format
MTP_FORMAT_BMP =                                 0x3804   # Microsoft Windows Bitmap file
MTP_FORMAT_CIFF =                                0x3805   # Canon Camera Image File Format
MTP_FORMAT_GIF =                                 0x3807   # Graphics Interchange Format
MTP_FORMAT_JFIF =                                0x3808   # JPEG File Interchange Format
MTP_FORMAT_CD =                                  0x3809   # PhotoCD Image Pac
MTP_FORMAT_PICT =                                0x380A   # Quickdraw Image Format
MTP_FORMAT_PNG =                                 0x380B   # Portable Network Graphics
MTP_FORMAT_TIFF =                                0x380D   # Tag Image File Format
MTP_FORMAT_TIFF_IT =                             0x380E   # Tag Image File Format for Information Technology (graphic arts)
MTP_FORMAT_JP2 =                                 0x380F   # JPEG2000 Baseline File Format
MTP_FORMAT_JPX =                                 0x3810   # JPEG2000 Extended File Format
MTP_FORMAT_UNDEFINED_FIRMWARE =                  0xB802
MTP_FORMAT_WINDOWS_IMAGE_FORMAT =                0xB881
MTP_FORMAT_UNDEFINED_AUDIO =                     0xB900
MTP_FORMAT_WMA =                                 0xB901
MTP_FORMAT_OGG =                                 0xB902
MTP_FORMAT_AAC =                                 0xB903
MTP_FORMAT_AUDIBLE =                             0xB904
MTP_FORMAT_FLAC =                                0xB906
MTP_FORMAT_UNDEFINED_VIDEO =                     0xB980
MTP_FORMAT_WMV =                                 0xB981
MTP_FORMAT_MP4_CONTAINER =                       0xB982  # ISO 14496-1
MTP_FORMAT_MP2 =                                 0xB983
MTP_FORMAT_3GP_CONTAINER =                       0xB984  # 3GPP file format. Details: http://www.3gpp.org/ftp/Specs/html-info/26244.htm (page title - \u201cTransparent end-to-end packet switched streaming service, 3GPP file format\u201d).
MTP_FORMAT_UNDEFINED_COLLECTION =                0xBA00
MTP_FORMAT_ABSTRACT_MULTIMEDIA_ALBUM =           0xBA01
MTP_FORMAT_ABSTRACT_IMAGE_ALBUM =                0xBA02
MTP_FORMAT_ABSTRACT_AUDIO_ALBUM =                0xBA03
MTP_FORMAT_ABSTRACT_VIDEO_ALBUM =                0xBA04
MTP_FORMAT_ABSTRACT_AV_PLAYLIST =                0xBA05
MTP_FORMAT_ABSTRACT_CONTACT_GROUP =              0xBA06
MTP_FORMAT_ABSTRACT_MESSAGE_FOLDER =             0xBA07
MTP_FORMAT_ABSTRACT_CHAPTERED_PRODUCTION =       0xBA08
MTP_FORMAT_ABSTRACT_AUDIO_PLAYLIST =             0xBA09
MTP_FORMAT_ABSTRACT_VIDEO_PLAYLIST =             0xBA0A
MTP_FORMAT_ABSTRACT_MEDIACAST =                  0xBA0B # For use with mediacasts; references multimedia enclosures of RSS feeds or episodic content
MTP_FORMAT_WPL_PLAYLIST =                        0xBA10
MTP_FORMAT_M3U_PLAYLIST =                        0xBA11
MTP_FORMAT_MPL_PLAYLIST =                        0xBA12
MTP_FORMAT_ASX_PLAYLIST =                        0xBA13
MTP_FORMAT_PLS_PLAYLIST =                        0xBA14
MTP_FORMAT_UNDEFINED_DOCUMENT =                  0xBA80
MTP_FORMAT_ABSTRACT_DOCUMENT =                   0xBA81
MTP_FORMAT_XML_DOCUMENT =                        0xBA82
MTP_FORMAT_MS_WORD_DOCUMENT =                    0xBA83
MTP_FORMAT_MHT_COMPILED_HTML_DOCUMENT =          0xBA84
MTP_FORMAT_MS_EXCEL_SPREADSHEET =                0xBA85
MTP_FORMAT_MS_POWERPOINT_PRESENTATION =          0xBA86
MTP_FORMAT_UNDEFINED_MESSAGE =                   0xBB00
MTP_FORMAT_ABSTRACT_MESSSAGE =                   0xBB01
MTP_FORMAT_UNDEFINED_CONTACT =                   0xBB80
MTP_FORMAT_ABSTRACT_CONTACT =                    0xBB81
MTP_FORMAT_VCARD_2 =                             0xBB82

# MTP Object Property Codes
MTP_PROPERTY_STORAGE_ID =                            0xDC01
MTP_PROPERTY_OBJECT_FORMAT =                         0xDC02
MTP_PROPERTY_PROTECTION_STATUS =                     0xDC03
MTP_PROPERTY_OBJECT_SIZE =                           0xDC04
MTP_PROPERTY_ASSOCIATION_TYPE =                      0xDC05
MTP_PROPERTY_ASSOCIATION_DESC =                      0xDC06
MTP_PROPERTY_OBJECT_FILE_NAME =                      0xDC07
MTP_PROPERTY_DATE_CREATED =                          0xDC08
MTP_PROPERTY_DATE_MODIFIED =                         0xDC09
MTP_PROPERTY_KEYWORDS =                              0xDC0A
MTP_PROPERTY_PARENT_OBJECT =                         0xDC0B
MTP_PROPERTY_ALLOWED_FOLDER_CONTENTS =               0xDC0C
MTP_PROPERTY_HIDDEN =                                0xDC0D
MTP_PROPERTY_SYSTEM_OBJECT =                         0xDC0E
MTP_PROPERTY_PERSISTENT_UID =                        0xDC41
MTP_PROPERTY_SYNC_ID =                               0xDC42
MTP_PROPERTY_PROPERTY_BAG =                          0xDC43
MTP_PROPERTY_NAME =                                  0xDC44
MTP_PROPERTY_CREATED_BY =                            0xDC45
MTP_PROPERTY_ARTIST =                                0xDC46
MTP_PROPERTY_DATE_AUTHORED =                         0xDC47
MTP_PROPERTY_DESCRIPTION =                           0xDC48
MTP_PROPERTY_URL_REFERENCE =                         0xDC49
MTP_PROPERTY_LANGUAGE_LOCALE =                       0xDC4A
MTP_PROPERTY_COPYRIGHT_INFORMATION =                 0xDC4B
MTP_PROPERTY_SOURCE =                                0xDC4C
MTP_PROPERTY_ORIGIN_LOCATION =                       0xDC4D
MTP_PROPERTY_DATE_ADDED =                            0xDC4E
MTP_PROPERTY_NON_CONSUMABLE =                        0xDC4F
MTP_PROPERTY_CORRUPT_UNPLAYABLE =                    0xDC50
MTP_PROPERTY_PRODUCER_SERIAL_NUMBER =                0xDC51
MTP_PROPERTY_REPRESENTATIVE_SAMPLE_FORMAT =          0xDC81
MTP_PROPERTY_REPRESENTATIVE_SAMPLE_SIZE =            0xDC82
MTP_PROPERTY_REPRESENTATIVE_SAMPLE_HEIGHT =          0xDC83
MTP_PROPERTY_REPRESENTATIVE_SAMPLE_WIDTH =           0xDC84
MTP_PROPERTY_REPRESENTATIVE_SAMPLE_DURATION =        0xDC85
MTP_PROPERTY_REPRESENTATIVE_SAMPLE_DATA =            0xDC86
MTP_PROPERTY_WIDTH =                                 0xDC87
MTP_PROPERTY_HEIGHT =                                0xDC88
MTP_PROPERTY_DURATION =                              0xDC89
MTP_PROPERTY_RATING =                                0xDC8A
MTP_PROPERTY_TRACK =                                 0xDC8B
MTP_PROPERTY_GENRE =                                 0xDC8C
MTP_PROPERTY_CREDITS =                               0xDC8D
MTP_PROPERTY_LYRICS =                                0xDC8E
MTP_PROPERTY_SUBSCRIPTION_CONTENT_ID =               0xDC8F
MTP_PROPERTY_PRODUCED_BY =                           0xDC90
MTP_PROPERTY_USE_COUNT =                             0xDC91
MTP_PROPERTY_SKIP_COUNT =                            0xDC92
MTP_PROPERTY_LAST_ACCESSED =                         0xDC93
MTP_PROPERTY_PARENTAL_RATING =                       0xDC94
MTP_PROPERTY_META_GENRE =                            0xDC95
MTP_PROPERTY_COMPOSER =                              0xDC96
MTP_PROPERTY_EFFECTIVE_RATING =                      0xDC97
MTP_PROPERTY_SUBTITLE =                              0xDC98
MTP_PROPERTY_ORIGINAL_RELEASE_DATE =                 0xDC99
MTP_PROPERTY_ALBUM_NAME =                            0xDC9A
MTP_PROPERTY_ALBUM_ARTIST =                          0xDC9B
MTP_PROPERTY_MOOD =                                  0xDC9C
MTP_PROPERTY_DRM_STATUS =                            0xDC9D
MTP_PROPERTY_SUB_DESCRIPTION =                       0xDC9E
MTP_PROPERTY_IS_CROPPED =                            0xDCD1
MTP_PROPERTY_IS_COLOUR_CORRECTED =                   0xDCD2
MTP_PROPERTY_IMAGE_BIT_DEPTH =                       0xDCD3
MTP_PROPERTY_F_NUMBER =                              0xDCD4
MTP_PROPERTY_EXPOSURE_TIME =                         0xDCD5
MTP_PROPERTY_EXPOSURE_INDEX =                        0xDCD6
MTP_PROPERTY_TOTAL_BITRATE =                         0xDE91
MTP_PROPERTY_BITRATE_TYPE =                          0xDE92
MTP_PROPERTY_SAMPLE_RATE =                           0xDE93
MTP_PROPERTY_NUMBER_OF_CHANNELS =                    0xDE94
MTP_PROPERTY_AUDIO_BIT_DEPTH =                       0xDE95
MTP_PROPERTY_SCAN_TYPE =                             0xDE97
MTP_PROPERTY_AUDIO_WAVE_CODEC =                      0xDE99
MTP_PROPERTY_AUDIO_BITRATE =                         0xDE9A
MTP_PROPERTY_VIDEO_FOURCC_CODEC =                    0xDE9B
MTP_PROPERTY_VIDEO_BITRATE =                         0xDE9C
MTP_PROPERTY_FRAMES_PER_THOUSAND_SECONDS =           0xDE9D
MTP_PROPERTY_KEYFRAME_DISTANCE =                     0xDE9E
MTP_PROPERTY_BUFFER_SIZE =                           0xDE9F
MTP_PROPERTY_ENCODING_QUALITY =                      0xDEA0
MTP_PROPERTY_ENCODING_PROFILE =                      0xDEA1
MTP_PROPERTY_DISPLAY_NAME =                          0xDCE0
MTP_PROPERTY_BODY_TEXT =                             0xDCE1
MTP_PROPERTY_SUBJECT =                               0xDCE2
MTP_PROPERTY_PRIORITY =                              0xDCE3
MTP_PROPERTY_GIVEN_NAME =                            0xDD00
MTP_PROPERTY_MIDDLE_NAMES =                          0xDD01
MTP_PROPERTY_FAMILY_NAME =                           0xDD02
MTP_PROPERTY_PREFIX =                                0xDD03
MTP_PROPERTY_SUFFIX =                                0xDD04
MTP_PROPERTY_PHONETIC_GIVEN_NAME =                   0xDD05
MTP_PROPERTY_PHONETIC_FAMILY_NAME =                  0xDD06
MTP_PROPERTY_EMAIL_PRIMARY =                         0xDD07
MTP_PROPERTY_EMAIL_PERSONAL_1 =                      0xDD08
MTP_PROPERTY_EMAIL_PERSONAL_2 =                      0xDD09
MTP_PROPERTY_EMAIL_BUSINESS_1 =                      0xDD0A
MTP_PROPERTY_EMAIL_BUSINESS_2 =                      0xDD0B
MTP_PROPERTY_EMAIL_OTHERS =                          0xDD0C
MTP_PROPERTY_PHONE_NUMBER_PRIMARY =                  0xDD0D
MTP_PROPERTY_PHONE_NUMBER_PERSONAL =                 0xDD0E
MTP_PROPERTY_PHONE_NUMBER_PERSONAL_2 =               0xDD0F
MTP_PROPERTY_PHONE_NUMBER_BUSINESS =                 0xDD10
MTP_PROPERTY_PHONE_NUMBER_BUSINESS_2 =               0xDD11
MTP_PROPERTY_PHONE_NUMBER_MOBILE =                   0xDD12
MTP_PROPERTY_PHONE_NUMBER_MOBILE_2 =                 0xDD13
MTP_PROPERTY_FAX_NUMBER_PRIMARY =                    0xDD14
MTP_PROPERTY_FAX_NUMBER_PERSONAL =                   0xDD15
MTP_PROPERTY_FAX_NUMBER_BUSINESS =                   0xDD16
MTP_PROPERTY_PAGER_NUMBER =                          0xDD17
MTP_PROPERTY_PHONE_NUMBER_OTHERS =                   0xDD18
MTP_PROPERTY_PRIMARY_WEB_ADDRESS =                   0xDD19
MTP_PROPERTY_PERSONAL_WEB_ADDRESS =                  0xDD1A
MTP_PROPERTY_BUSINESS_WEB_ADDRESS =                  0xDD1B
MTP_PROPERTY_INSTANT_MESSANGER_ADDRESS =             0xDD1C
MTP_PROPERTY_INSTANT_MESSANGER_ADDRESS_2 =           0xDD1D
MTP_PROPERTY_INSTANT_MESSANGER_ADDRESS_3 =           0xDD1E
MTP_PROPERTY_POSTAL_ADDRESS_PERSONAL_FULL =          0xDD1F
MTP_PROPERTY_POSTAL_ADDRESS_PERSONAL_LINE_1 =        0xDD20
MTP_PROPERTY_POSTAL_ADDRESS_PERSONAL_LINE_2 =        0xDD21
MTP_PROPERTY_POSTAL_ADDRESS_PERSONAL_CITY =          0xDD22
MTP_PROPERTY_POSTAL_ADDRESS_PERSONAL_REGION =        0xDD23
MTP_PROPERTY_POSTAL_ADDRESS_PERSONAL_POSTAL_CODE =   0xDD24
MTP_PROPERTY_POSTAL_ADDRESS_PERSONAL_COUNTRY =       0xDD25
MTP_PROPERTY_POSTAL_ADDRESS_BUSINESS_FULL =          0xDD26
MTP_PROPERTY_POSTAL_ADDRESS_BUSINESS_LINE_1 =        0xDD27
MTP_PROPERTY_POSTAL_ADDRESS_BUSINESS_LINE_2 =        0xDD28
MTP_PROPERTY_POSTAL_ADDRESS_BUSINESS_CITY =          0xDD29
MTP_PROPERTY_POSTAL_ADDRESS_BUSINESS_REGION =        0xDD2A
MTP_PROPERTY_POSTAL_ADDRESS_BUSINESS_POSTAL_CODE =   0xDD2B
MTP_PROPERTY_POSTAL_ADDRESS_BUSINESS_COUNTRY =       0xDD2C
MTP_PROPERTY_POSTAL_ADDRESS_OTHER_FULL =             0xDD2D
MTP_PROPERTY_POSTAL_ADDRESS_OTHER_LINE_1 =           0xDD2E
MTP_PROPERTY_POSTAL_ADDRESS_OTHER_LINE_2 =           0xDD2F
MTP_PROPERTY_POSTAL_ADDRESS_OTHER_CITY =             0xDD30
MTP_PROPERTY_POSTAL_ADDRESS_OTHER_REGION =           0xDD31
MTP_PROPERTY_POSTAL_ADDRESS_OTHER_POSTAL_CODE =      0xDD32
MTP_PROPERTY_POSTAL_ADDRESS_OTHER_COUNTRY =          0xDD33
MTP_PROPERTY_ORGANIZATION_NAME =                     0xDD34
MTP_PROPERTY_PHONETIC_ORGANIZATION_NAME =            0xDD35
MTP_PROPERTY_ROLE =                                  0xDD36
MTP_PROPERTY_BIRTHDATE =                             0xDD37
MTP_PROPERTY_MESSAGE_TO =                            0xDD40
MTP_PROPERTY_MESSAGE_CC =                            0xDD41
MTP_PROPERTY_MESSAGE_BCC =                           0xDD42
MTP_PROPERTY_MESSAGE_READ =                          0xDD43
MTP_PROPERTY_MESSAGE_RECEIVED_TIME =                 0xDD44
MTP_PROPERTY_MESSAGE_SENDER =                        0xDD45
MTP_PROPERTY_ACTIVITY_BEGIN_TIME =                   0xDD50
MTP_PROPERTY_ACTIVITY_END_TIME =                     0xDD51
MTP_PROPERTY_ACTIVITY_LOCATION =                     0xDD52
MTP_PROPERTY_ACTIVITY_REQUIRED_ATTENDEES =           0xDD54
MTP_PROPERTY_ACTIVITY_OPTIONAL_ATTENDEES =           0xDD55
MTP_PROPERTY_ACTIVITY_RESOURCES =                    0xDD56
MTP_PROPERTY_ACTIVITY_ACCEPTED =                     0xDD57
MTP_PROPERTY_ACTIVITY_TENTATIVE =                    0xDD58
MTP_PROPERTY_ACTIVITY_DECLINED =                     0xDD59
MTP_PROPERTY_ACTIVITY_REMAINDER_TIME =               0xDD5A
MTP_PROPERTY_ACTIVITY_OWNER =                        0xDD5B
MTP_PROPERTY_ACTIVITY_STATUS =                       0xDD5C
MTP_PROPERTY_OWNER =                                 0xDD5D
MTP_PROPERTY_EDITOR =                                0xDD5E
MTP_PROPERTY_WEBMASTER =                             0xDD5F
MTP_PROPERTY_URL_SOURCE =                            0xDD60
MTP_PROPERTY_URL_DESTINATION =                       0xDD61
MTP_PROPERTY_TIME_BOOKMARK =                         0xDD62
MTP_PROPERTY_OBJECT_BOOKMARK =                       0xDD63
MTP_PROPERTY_BYTE_BOOKMARK =                         0xDD64
MTP_PROPERTY_LAST_BUILD_DATE =                       0xDD70
MTP_PROPERTY_TIME_TO_LIVE =                          0xDD71
MTP_PROPERTY_MEDIA_GUID =                            0xDD72

# MTP Device Property Codes
MTP_DEVICE_PROPERTY_UNDEFINED =                      0x5000
MTP_DEVICE_PROPERTY_BATTERY_LEVEL =                  0x5001
MTP_DEVICE_PROPERTY_FUNCTIONAL_MODE =                0x5002
MTP_DEVICE_PROPERTY_IMAGE_SIZE =                     0x5003
MTP_DEVICE_PROPERTY_COMPRESSION_SETTING =            0x5004
MTP_DEVICE_PROPERTY_WHITE_BALANCE =                  0x5005
MTP_DEVICE_PROPERTY_RGB_GAIN =                       0x5006
MTP_DEVICE_PROPERTY_F_NUMBER =                       0x5007
MTP_DEVICE_PROPERTY_FOCAL_LENGTH =                   0x5008
MTP_DEVICE_PROPERTY_FOCUS_DISTANCE =                 0x5009
MTP_DEVICE_PROPERTY_FOCUS_MODE =                     0x500A
MTP_DEVICE_PROPERTY_EXPOSURE_METERING_MODE =         0x500B
MTP_DEVICE_PROPERTY_FLASH_MODE =                     0x500C
MTP_DEVICE_PROPERTY_EXPOSURE_TIME =                  0x500D
MTP_DEVICE_PROPERTY_EXPOSURE_PROGRAM_MODE =          0x500E
MTP_DEVICE_PROPERTY_EXPOSURE_INDEX =                 0x500F
MTP_DEVICE_PROPERTY_EXPOSURE_BIAS_COMPENSATION =     0x5010
MTP_DEVICE_PROPERTY_DATETIME =                       0x5011
MTP_DEVICE_PROPERTY_CAPTURE_DELAY =                  0x5012
MTP_DEVICE_PROPERTY_STILL_CAPTURE_MODE =             0x5013
MTP_DEVICE_PROPERTY_CONTRAST =                       0x5014
MTP_DEVICE_PROPERTY_SHARPNESS =                      0x5015
MTP_DEVICE_PROPERTY_DIGITAL_ZOOM =                   0x5016
MTP_DEVICE_PROPERTY_EFFECT_MODE =                    0x5017
MTP_DEVICE_PROPERTY_BURST_NUMBER =                   0x5018
MTP_DEVICE_PROPERTY_BURST_INTERVAL =                 0x5019
MTP_DEVICE_PROPERTY_TIMELAPSE_NUMBER =               0x501A
MTP_DEVICE_PROPERTY_TIMELAPSE_INTERVAL =             0x501B
MTP_DEVICE_PROPERTY_FOCUS_METERING_MODE =            0x501C
MTP_DEVICE_PROPERTY_UPLOAD_URL =                     0x501D
MTP_DEVICE_PROPERTY_ARTIST =                         0x501E
MTP_DEVICE_PROPERTY_COPYRIGHT_INFO =                 0x501F
MTP_DEVICE_PROPERTY_SYNCHRONIZATION_PARTNER =        0xD401
MTP_DEVICE_PROPERTY_DEVICE_FRIENDLY_NAME =           0xD402
MTP_DEVICE_PROPERTY_VOLUME =                         0xD403
MTP_DEVICE_PROPERTY_SUPPORTED_FORMATS_ORDERED =      0xD404
MTP_DEVICE_PROPERTY_DEVICE_ICON =                    0xD405
MTP_DEVICE_PROPERTY_PLAYBACK_RATE =                  0xD410
MTP_DEVICE_PROPERTY_PLAYBACK_OBJECT =                0xD411
MTP_DEVICE_PROPERTY_PLAYBACK_CONTAINER_INDEX =       0xD412
MTP_DEVICE_PROPERTY_SESSION_INITIATOR_VERSION_INFO = 0xD406
MTP_DEVICE_PROPERTY_PERCEIVED_DEVICE_TYPE =          0xD407

# MTP Operation Codes
MTP_OPERATION_GET_DEVICE_INFO =                      0x1001
MTP_OPERATION_OPEN_SESSION =                         0x1002
MTP_OPERATION_CLOSE_SESSION =                        0x1003
MTP_OPERATION_GET_STORAGE_IDS =                      0x1004
MTP_OPERATION_GET_STORAGE_INFO =                     0x1005
MTP_OPERATION_GET_NUM_OBJECTS =                      0x1006
MTP_OPERATION_GET_OBJECT_HANDLES =                   0x1007
MTP_OPERATION_GET_OBJECT_INFO =                      0x1008
MTP_OPERATION_GET_OBJECT =                           0x1009
MTP_OPERATION_GET_THUMB =                            0x100A
MTP_OPERATION_DELETE_OBJECT =                        0x100B
MTP_OPERATION_SEND_OBJECT_INFO =                     0x100C
MTP_OPERATION_SEND_OBJECT =                          0x100D
MTP_OPERATION_INITIATE_CAPTURE =                     0x100E
MTP_OPERATION_FORMAT_STORE =                         0x100F
MTP_OPERATION_RESET_DEVICE =                         0x1010
MTP_OPERATION_SELF_TEST =                            0x1011
MTP_OPERATION_SET_OBJECT_PROTECTION =                0x1012
MTP_OPERATION_POWER_DOWN =                           0x1013
MTP_OPERATION_GET_DEVICE_PROP_DESC =                 0x1014
MTP_OPERATION_GET_DEVICE_PROP_VALUE =                0x1015
MTP_OPERATION_SET_DEVICE_PROP_VALUE =                0x1016
MTP_OPERATION_RESET_DEVICE_PROP_VALUE =              0x1017
MTP_OPERATION_TERMINATE_OPEN_CAPTURE =               0x1018
MTP_OPERATION_MOVE_OBJECT =                          0x1019
MTP_OPERATION_COPY_OBJECT =                          0x101A
MTP_OPERATION_GET_PARTIAL_OBJECT =                   0x101B
MTP_OPERATION_INITIATE_OPEN_CAPTURE =                0x101C
MTP_OPERATION_GET_OBJECT_PROPS_SUPPORTED =           0x9801
MTP_OPERATION_GET_OBJECT_PROP_DESC =                 0x9802
MTP_OPERATION_GET_OBJECT_PROP_VALUE =                0x9803
MTP_OPERATION_SET_OBJECT_PROP_VALUE =                0x9804
MTP_OPERATION_GET_OBJECT_PROP_LIST =                 0x9805
MTP_OPERATION_SET_OBJECT_PROP_LIST =                 0x9806
MTP_OPERATION_GET_INTERDEPENDENT_PROP_DESC =         0x9807
MTP_OPERATION_SEND_OBJECT_PROP_LIST =                0x9808
MTP_OPERATION_GET_OBJECT_REFERENCES =                0x9810
MTP_OPERATION_SET_OBJECT_REFERENCES =                0x9811
MTP_OPERATION_SKIP =                                 0x9820

# Android extensions for direct file IO

# Same as GetPartialObject, but with 64 bit offset
MTP_OPERATION_GET_PARTIAL_OBJECT_64 =                0x95C1
# Same as GetPartialObject64, but copying host to device
MTP_OPERATION_SEND_PARTIAL_OBJECT =                  0x95C2
# Truncates file to 64 bit length
MTP_OPERATION_TRUNCATE_OBJECT =                      0x95C3
# Must be called before using SendPartialObject and TruncateObject
MTP_OPERATION_BEGIN_EDIT_OBJECT =                    0x95C4
# Called to commit changes made by SendPartialObject and TruncateObject
MTP_OPERATION_END_EDIT_OBJECT =                      0x95C5

# MTP Response Codes
MTP_RESPONSE_UNDEFINED =                                 0x2000
MTP_RESPONSE_OK =                                        0x2001
MTP_RESPONSE_GENERAL_ERROR =                             0x2002
MTP_RESPONSE_SESSION_NOT_OPEN =                          0x2003
MTP_RESPONSE_INVALID_TRANSACTION_ID =                    0x2004
MTP_RESPONSE_OPERATION_NOT_SUPPORTED =                   0x2005
MTP_RESPONSE_PARAMETER_NOT_SUPPORTED =                   0x2006
MTP_RESPONSE_INCOMPLETE_TRANSFER =                       0x2007
MTP_RESPONSE_INVALID_STORAGE_ID =                        0x2008
MTP_RESPONSE_INVALID_OBJECT_HANDLE =                     0x2009
MTP_RESPONSE_DEVICE_PROP_NOT_SUPPORTED =                 0x200A
MTP_RESPONSE_INVALID_OBJECT_FORMAT_CODE =                0x200B
MTP_RESPONSE_STORAGE_FULL =                              0x200C
MTP_RESPONSE_OBJECT_WRITE_PROTECTED =                    0x200D
MTP_RESPONSE_STORE_READ_ONLY =                           0x200E
MTP_RESPONSE_ACCESS_DENIED =                             0x200F
MTP_RESPONSE_NO_THUMBNAIL_PRESENT =                      0x2010
MTP_RESPONSE_SELF_TEST_FAILED =                          0x2011
MTP_RESPONSE_PARTIAL_DELETION =                          0x2012
MTP_RESPONSE_STORE_NOT_AVAILABLE =                       0x2013
MTP_RESPONSE_SPECIFICATION_BY_FORMAT_UNSUPPORTED =       0x2014
MTP_RESPONSE_NO_VALID_OBJECT_INFO =                      0x2015
MTP_RESPONSE_INVALID_CODE_FORMAT =                       0x2016
MTP_RESPONSE_UNKNOWN_VENDOR_CODE =                       0x2017
MTP_RESPONSE_CAPTURE_ALREADY_TERMINATED =                0x2018
MTP_RESPONSE_DEVICE_BUSY =                               0x2019
MTP_RESPONSE_INVALID_PARENT_OBJECT =                     0x201A
MTP_RESPONSE_INVALID_DEVICE_PROP_FORMAT =                0x201B
MTP_RESPONSE_INVALID_DEVICE_PROP_VALUE =                 0x201C
MTP_RESPONSE_INVALID_PARAMETER =                         0x201D
MTP_RESPONSE_SESSION_ALREADY_OPEN =                      0x201E
MTP_RESPONSE_TRANSACTION_CANCELLED =                     0x201F
MTP_RESPONSE_SPECIFICATION_OF_DESTINATION_UNSUPPORTED =  0x2020
MTP_RESPONSE_INVALID_OBJECT_PROP_CODE =                  0xA801
MTP_RESPONSE_INVALID_OBJECT_PROP_FORMAT =                0xA802
MTP_RESPONSE_INVALID_OBJECT_PROP_VALUE =                 0xA803
MTP_RESPONSE_INVALID_OBJECT_REFERENCE =                  0xA804
MTP_RESPONSE_GROUP_NOT_SUPPORTED =                       0xA805
MTP_RESPONSE_INVALID_DATASET =                           0xA806
MTP_RESPONSE_SPECIFICATION_BY_GROUP_UNSUPPORTED =        0xA807
MTP_RESPONSE_SPECIFICATION_BY_DEPTH_UNSUPPORTED =        0xA808
MTP_RESPONSE_OBJECT_TOO_LARGE =                          0xA809
MTP_RESPONSE_OBJECT_PROP_NOT_SUPPORTED =                 0xA80A

# MTP Event Codes
MTP_EVENT_UNDEFINED =                        0x4000
MTP_EVENT_CANCEL_TRANSACTION =               0x4001
MTP_EVENT_OBJECT_ADDED =                     0x4002
MTP_EVENT_OBJECT_REMOVED =                   0x4003
MTP_EVENT_STORE_ADDED =                      0x4004
MTP_EVENT_STORE_REMOVED =                    0x4005
MTP_EVENT_DEVICE_PROP_CHANGED =              0x4006
MTP_EVENT_OBJECT_INFO_CHANGED =              0x4007
MTP_EVENT_DEVICE_INFO_CHANGED =              0x4008
MTP_EVENT_REQUEST_OBJECT_TRANSFER =          0x4009
MTP_EVENT_STORE_FULL =                       0x400A
MTP_EVENT_DEVICE_RESET =                     0x400B
MTP_EVENT_STORAGE_INFO_CHANGED =             0x400C
MTP_EVENT_CAPTURE_COMPLETE =                 0x400D
MTP_EVENT_UNREPORTED_STATUS =                0x400E
MTP_EVENT_OBJECT_PROP_CHANGED =              0xC801
MTP_EVENT_OBJECT_PROP_DESC_CHANGED =         0xC802
MTP_EVENT_OBJECT_REFERENCES_CHANGED =        0xC803

# Storage Type
MTP_STORAGE_FIXED_ROM =                      0x0001
MTP_STORAGE_REMOVABLE_ROM =                  0x0002
MTP_STORAGE_FIXED_RAM =                      0x0003
MTP_STORAGE_REMOVABLE_RAM =                  0x0004

# Storage File System
MTP_STORAGE_FILESYSTEM_FLAT =                0x0001
MTP_STORAGE_FILESYSTEM_HIERARCHICAL =        0x0002
MTP_STORAGE_FILESYSTEM_DCF =                 0x0003

# Storage Access Capability
MTP_STORAGE_READ_WRITE =                     0x0000
MTP_STORAGE_READ_ONLY_WITHOUT_DELETE =       0x0001
MTP_STORAGE_READ_ONLY_WITH_DELETE =          0x0002

# Association Type
MTP_ASSOCIATION_TYPE_UNDEFINED =             0x0000
MTP_ASSOCIATION_TYPE_GENERIC_FOLDER =        0x0001

