import usb.core
from usb.backend import libusb1
import usb.util
import time


def usbdebug():
    import os

    os.environ["PYUSB_DEBUG"] = "debug"
    import usb.core

    print(usb.core.find())


if __name__ == "__main__":
    usbdebug()
    dev = usb.core.find(idVendor=0x2B87, idProduct=0x0001)
    if dev is None:
        print(usb.core.USBError)
        raise ValueError("Device not found")

    msgs = ["000000120101", "000000120302"]
    for msg in msgs:
        dev.write(2, msg)
        time.sleep(0.5)

    for i in range(10):
        try:
            ret = dev.read(130, 24, 100)
            print(f"{len(ret)}")
            sret = "".join(f"{x:02x}" for x in ret)
            sret2 = "".join([chr(x) for x in ret])
            print(f"usbrx: {sret2} {sret}")
        except usb.core.USBError as e:
            if "time" not in str(e):
                print(f"USB: {e}")
            continue