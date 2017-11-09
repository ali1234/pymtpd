from __future__ import print_function

import select

import functionfs
import functionfs.ch9

from .responder import MTPResponder

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
                0x0409: [
                    u'MTP',
                ],
            },
        )

        self.inep = self._ep_list[1]
        self.outep = self._ep_list[2]
        self.intep = self._ep_list[3]

        assert len(self._ep_list) == 4
        self.responder = MTPResponder(
            outep=self.outep,
            inep=self.inep,
            intep=self.intep,
        )

    def processEventsForever(self):
        while True:
            (r, w, x) = select.select([self.ep0, self.outep], [], [])
            if self.ep0 in r:
                self.processEvents()
            if self.outep in r:
                self.responder.handleOneOperation()

