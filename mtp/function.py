import asyncio

import functionfs
import functionfs.ch9

from mtp.kaio import KAIOReader, KAIOWriter
from mtp.responder import MTPResponder

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

        self.loop = asyncio.get_event_loop()
        self.loop.set_exception_handler(self.exception)

        try:
            # If anything goes wrong from here on we MUST not
            # hold any file descriptors open, else there is a
            # good chance the kernel will deadlock.
            super(MTPFunction, self).__init__(
                path,
                fs_list=fs_list,
                hs_list=hs_list,
                lang_dict={
                    0x0409: [
                        u'MTP',
                    ],
                },
            )

            self.loop.add_reader(self.ep0, self.processEvents)

            assert len(self._ep_list) == 4

            self.inep = self._ep_list[1]
            self.outep = KAIOReader(self._ep_list[2])
            self.intep = KAIOWriter(self._ep_list[3])

            self.outep.maxpkt = 512
            self.inep.maxpkt = 512

            self.responder = MTPResponder(
                outep=self.outep,
                inep=self.inep,
                intep=self.intep,
                loop=self.loop,
            )

        except:
            # Catch ANY exception, close all file descriptors
            # and then re-raise.
            self.close()
            raise

    def exception(self, loop, context):
        loop.stop()
        raise context['exception']

    def close(self):
        self.outep.close()
        self.intep.close()
        super().close()

    def processEventsForever(self):
        self.outep.submit() # prime the first async read
        self.loop.run_forever()
