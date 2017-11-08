import functionfs
import functionfs.ch9

from mtpthread import MTPThread

FS_BULK_MAX_PACKET_SIZE = 64
HS_BULK_MAX_PACKET_SIZE = 512

class MTPFunction(functionfs.Function):
    def __init__(self, path):

        INTERFACE_DESCRIPTOR = functionfs.getDescriptor(
            functionfs.USBInterfaceDescriptor,
            bInterfaceNumber=0,
            bAlternateSetting=0,
            bNumEndpoints=3,
            bInterfaceClass=functionfs.ch9.USB_CLASS_VENDOR_SPEC,
            bInterfaceSubClass=functionfs.ch9.USB_SUBCLASS_VENDOR_SPEC,
            bInterfaceProtocol=0,
            iInterface=1,
        )
        fs_list = [INTERFACE_DESCRIPTOR]
        hs_list = [INTERFACE_DESCRIPTOR]
        fs_list.append(
            functionfs.getDescriptor(
                functionfs.USBEndpointDescriptorNoAudio,
                bEndpointAddress=1|functionfs.ch9.USB_DIR_IN,
                bmAttributes=functionfs.ch9.USB_ENDPOINT_XFER_BULK,
                wMaxPacketSize=FS_BULK_MAX_PACKET_SIZE,
                bInterval=0,
            )
        )
        fs_list.append(
            functionfs.getDescriptor(
                functionfs.USBEndpointDescriptorNoAudio,
                bEndpointAddress=2|functionfs.ch9.USB_DIR_OUT,
                bmAttributes=functionfs.ch9.USB_ENDPOINT_XFER_BULK,
                wMaxPacketSize=FS_BULK_MAX_PACKET_SIZE,
                bInterval=0,
            )
        )
        hs_list.append(
            functionfs.getDescriptor(
                functionfs.USBEndpointDescriptorNoAudio,
                bEndpointAddress=1|functionfs.ch9.USB_DIR_IN,
                bmAttributes=functionfs.ch9.USB_ENDPOINT_XFER_BULK,
                wMaxPacketSize=HS_BULK_MAX_PACKET_SIZE,
                bInterval=0,
            )
        )
        hs_list.append(
            functionfs.getDescriptor(
                functionfs.USBEndpointDescriptorNoAudio,
                bEndpointAddress=2|functionfs.ch9.USB_DIR_OUT,
                bmAttributes=functionfs.ch9.USB_ENDPOINT_XFER_BULK,
                wMaxPacketSize=HS_BULK_MAX_PACKET_SIZE,
                bInterval=0,
            )
        )

        INT_DESCRIPTOR = functionfs.getDescriptor(
            functionfs.USBEndpointDescriptorNoAudio,
            bEndpointAddress=2|functionfs.ch9.USB_DIR_IN,
            bmAttributes=functionfs.ch9.USB_ENDPOINT_XFER_INT,
            wMaxPacketSize=28,
            bInterval=6,
        )

        hs_list.append(INT_DESCRIPTOR)
        fs_list.append(INT_DESCRIPTOR)

        super(MTPFunction, self).__init__(
            path,
            fs_list=fs_list,
            hs_list=hs_list,
            lang_dict={
                0x0409: [x.decode('utf-8') for x in (
                    'MTP',
                )],
            },
        )

        assert len(self._ep_list) == 4
        thread_list = self.__thread_list = []
        thread_list.append(
            MTPThread(
                name='MTPThread',
                outep=self._ep_list[2],
                inep=self._ep_list[1],
                intep=self._ep_list[3],
            )
        )

    def onEnable(self):
        print 'functionfs: ENABLE'
        for thread in self.__thread_list:
            thread.start()

    def onDisable(self):
        print 'functionfs: DISABLE'

    def onBind(self):
        print 'functionfs: BIND'

    def onUnbind(self):
        print 'functionfs: UNBIND'

    def onSuspend(self):
        print 'functionfs: SUSPEND'

    def onResume(self):
        print 'functionfs: RESUME'

    def onSetup(self, request_type, request, value, index, length):
        super(MTPFunction, self).onSetup(
            request_type, request, value, index, length,
        )

