import usb.core
from usb.backend import libusb1
import usb.util
import logging
import asyncio
import json
from TestCubeUSB.TestCubeComponents.adc import AdcMessage
from TestCubeUSB.TestCubeComponents.pwm import PwmMessage
from TestCubeUSB.TestCubeComponents.relay import RelayMessage
from TestCubeUSB.TestCubeComponents.di import DiMessage
from TestCubeUSB.TestCubeComponents.actuators import ActCurMessage
from TestCubeUSB.TestCubeComponents.frequency import FrequencyMessage
from TestCubeUSB.TestCubeComponents.usb import UsbMessage
from TestCubeUSB.TestCubeComponents.can import CanDatabaseMessage
from TestCubeUSB.TestCubeComponents.version import VersionMessage
import copy

class TestCubeUSB(
    RelayMessage,
    PwmMessage,
    DiMessage,
    ActCurMessage,
    UsbMessage,
    FrequencyMessage,
    AdcMessage,
    CanDatabaseMessage,
    VersionMessage,
):
    def callParentInits(self):
        RelayMessage.__init__(self)
        PwmMessage.__init__(self)
        DiMessage.__init__(self)
        ActCurMessage.__init__(self)
        UsbMessage.__init__(self)
        FrequencyMessage.__init__(self)
        AdcMessage.__init__(self)
        VersionMessage.__init__(self)

    def __init__(self):
        self.logger = logging.getLogger("gizmoLogger")
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("init")
        self.callParentInits()
        self.callback = None
        self.version = None
        self.running = False
        self.ask = None
        self.getVersionEvent = None
        AdcMessage.__init__(self)
        self.usbrxcount=0
        self.usbidparsers = {
            "00000005": self.recusb_5_pwmfreq,
            "00000007": self.recusb_7_pwmdutycycle,
            "00000009": self.recusb_9_pwmenable,
            "0000000b": self.recusb_b_digitalinputs,
            "0000000d": self.recusb_00d_actcurrent,
            "0000010d": self.recusb_10d_actcurrent,
            "0000020d": self.recusb_20d_actcurrent,
            "0000030d": self.recusb_30d_actcurrent,
            "0000000f": self.recusb_00f_speed,
            "0000010f": self.recusb_10f_speed,
            "00000011": self.recusb_011_adc,
            "00000111": self.recusb_111_adc,
            "00000211": self.recusb_211_adc,
            "00000013": self.recusb_13_relay,
            "0000001d": self.recusb_1d_actfault,
            "00000051": self.recusb_51_version,
        }
        self.actcurrent_listinfirstmsg = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.adc_listinfirstmsg = []
        with open("TestCubeUSB/schema.json") as f:
            self.schema = json.load(f)

    def setcallback(self, callback):
        if not callable(callback):
            raise ValueError("callback must be a function")
        self.callback = callback

    def start(self):
        if self.callback is None:
            raise RuntimeError("controller callback not set")
        self.dev = None
        devs = usb.core.find(idVendor=0x2B87, idProduct=0x0001, find_all=True)
        if devs is not None:
            for dev in devs:
                try:
                    dev.write(2, "0000050")
                except Exception as e:
                    print(f"{e}")
                    continue
                self.dev = dev
                d = str(dev).split("\n")
                devdict = {}
                for line in d:
                    if 'DEVICE ID' in line:
                        s = line.split(" ")
                        #print(s)
                        devdict['deviceid'] = s[2]
                        devdict['bus'] = s[5] + "." + s[7]

                    elif ':' in line:
                        k,v = line.split(':')[0].strip(),line.split(':')[1].strip()
                        devdict[k] = v
                #print(devdict)
                self.callback({"path": "/usb/usbinfo", "data": devdict})
                return
        raise ValueError("Device not found")

    def finished(self):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f"finished")
        msgs = (
            self.get_relay_messages()
            + self.get_pwm_messages()
            + self.get_di_messages()
            + self.get_actcur_messages()
            + self.get_sendusb_messages()
            + self.get_freq_messages()
            + self.get_adc_messages()
            + self.get_version_messages()
        )
        for msg in msgs:
            if self.logger.isEnabledFor(logging.USB):
                self.logger.usb(f"finished: {msg}")
            self.dev.write(2, msg)
        self.callParentInits()

    async def usbrxhandler(self):
        if self.getVersionEvent is None:
            self.getVersionEvent = asyncio.Event()
        self.running = True
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("running")
        while 1:
            await asyncio.sleep(0.0001)
            try:
                msg = self.dev.read(130, 24, 100)
            except usb.core.USBError as e:
                if "time" not in str(e):
                    self.logger.error(f"ERROR: {e}")
                continue
            msg = "".join([chr(x) for x in msg])
            if self.logger.isEnabledFor(logging.USB):
                self.logger.usb(f"{msg}")
            self.usbrxcount += 1
            self.callback([{"path": "/usb/rxMessage", "data": msg},
                {"path": "/usb/rxCount" , "data": self.usbrxcount},
            ])

            d = self.recUsb(msg)
            if d is None:
                continue
            if len(d) > 0:
                self.callback(d)

    def recUsb(self, msg):
        _id, payload = msg[:8], msg[8:]
        try:
            f = self.usbidparsers.get(_id.lower())
            if self.logger.isEnabledFor(logging.USB):
                self.logger.usb(f"{f.__name__}")
            if f is None:
                self.logger.error(f"TescubeUSB: ID not found in {self.usbidparsers}")
                return []
        except Exception as e:
            self.logger.error(f"ERROR: {e}")
        if f is None:
            return []
        result = f(payload)
        return result
