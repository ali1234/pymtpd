#!/usr/bin/env python3

import os, subprocess, logging, argparse

import mtp

class MTPGadget(mtp.Gadget):

    def __enter__(self):
        print('Configuring gadget')
        self.gadget.bcdUSB = '0x0200'
        self.gadget.bDeviceClass = '0x02'
        self.gadget.bDeviceSubClass = '0x02'
        self.gadget.bcdDevice = '0x3008'
        self.gadget.idVendor = self.vid
        self.gadget.idProduct = self.pid

        self.gadget.os_desc.use = '1'
        self.gadget.os_desc.b_vendor_code = '0xcd'
        self.gadget.os_desc.qw_sign = 'MSFT100'

        self.gadget.strings['0x409'].serialnumber = self.serialnumber
        self.gadget.strings['0x409'].manufacturer = self.manufacturer
        self.gadget.strings['0x409'].product = self.product

        #self.gadget.functions['rndis.usb0'].os_desc['interface.rndis'].compatible_id = 'RNDIS'
        #self.gadget.functions['rndis.usb0'].os_desc['interface.rndis'].sub_compatible_id = '5162001'

        self.gadget.configs['c.1'].strings['0x409'].configuration = 'mtp test'

        #self.add_function_to_config('rndis.usb0', 'c.1')
        #self.add_function_to_config('acm.GS0', 'c.1')
        #self.add_function_to_config('acm.GS1', 'c.1')
        #self.add_function_to_config('acm.GS2', 'c.1')
        #self.add_function_to_config('acm.GS3', 'c.1')
        self.add_function_to_config('ffs.mtp', 'c.1')

        os.makedirs('/dev/mtp', exist_ok=True)

        subprocess.call(['mount', '-c', '-t', 'functionfs', 'mtp', '/dev/mtp'])

        return self

    def __exit__(self, t, value, traceback):
        print('Tearing down gadget')
        self.gadget.UDC = ''

        if(subprocess.call(['umount', '/dev/mtp'])):
            print('Can\'t teardown gadget because functonfs is still in use.')
            return

        #self.remove_function_from_config('rndis.usb0', 'c.1')
        #self.remove_function_from_config('acm.GS0', 'c.1')
        #self.remove_function_from_config('acm.GS1', 'c.1')
        #self.remove_function_from_config('acm.GS2', 'c.1')
        #self.remove_function_from_config('acm.GS3', 'c.1')
        self.remove_function_from_config('ffs.mtp', 'c.1')

        del self.gadget.configs['c.1'].strings['0x409']
        del self.gadget.configs['c.1']
        #del self.gadget.functions['rndis.usb0']
        #del self.gadget.functions['acm.GS0']
        #del self.gadget.functions['acm.GS1']
        #del self.gadget.functions['acm.GS2']
        #del self.gadget.functions['acm.GS3']
        del self.gadget.functions['ffs.mtp']
        del self.gadget.strings['0x409']

        self.remove_gadget()



def main():

    # TODO: command line options / config file for the following:
    #  MTP device name
    #  storage name/path (multiple times)
    #  udc device
    #  configfs dir

    parser = argparse.ArgumentParser(description='MTP Daemon.')
    parser.add_argument('--log-level', type=str, help='CRITICAL, ERROR, WARNING, INFO, DEBUG', default='WARN')
    parser.add_argument('--udc', type=str, help='UDC device. (dummy_udc.0)', default='dummy_udc.0')
    parser.add_argument('-s', '--storage', action='append', nargs=2, metavar=('name','path'), help='Add storage.')
    parser.add_argument('-n', '--name', type=str, help='MTP device name', default='MTP Device')

    parser.add_argument('-v', '--vid', type=str, help='MTP device name', default='0x0430')
    parser.add_argument('-p', '--pid', type=str, help='MTP device name', default='0xa4a2')
    parser.add_argument('-M', '--manufacturer', type=str, help='MTP device name', default='Nobody')
    parser.add_argument('-P', '--product', type=str, help='MTP device name', default='MTP Device')
    parser.add_argument('-S', '--serialnumber', type=str, help='MTP device name', default='12345678')

    args = parser.parse_args()

    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log_level)
    logging.basicConfig(level=numeric_level)

    with MTPGadget(name='g1', vid='0x0430', pid='0xa4a2',
                   manufacturer=args.manufacturer, product=args.product,
                   serialnumber=args.serialnumber) as g:
        with mtp.MTPFunction('/dev/mtp', args) as function:

            g.bind(args.udc)

            try:
                function.processEventsForever()
            except KeyboardInterrupt:
                print("Shutting down")


if __name__ == '__main__':
    main()