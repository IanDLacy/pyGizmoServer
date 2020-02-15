class UsbMessage:
    def __init__(self):
        self.usbmsg = None

    def sendrawusb(self, msg):
        self.usbmsg = msg
        print(f"sendrawusb({msg=})")

    def get_sendusb_messages(self):
        print(f"get_sendusb_messages()")
        if self.usbmsg is None:
            return []
        if isinstance(self.usbmsg,str):
            self.usbmsg = [self.usbmsg]
        print(f"get_sendusb_messages({self.usbmsg=})")     
        return self.usbmsg

