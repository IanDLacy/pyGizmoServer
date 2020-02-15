import logging


class AdcMessage:
    def __init__(self):
        self.AdcChannels = 0x3F
        self.AdcRate = None

    def setAdcMonitorUpdateRate(self, rate: int):
        self.AdcRate = int(rate / 50)

    def setAdcEnabled(self, enabled: bool, channel: int):
        if enabled:
            self.AdcChannels |= 1 << channel
        else:
            self.AdcChannels &= (1 << channel) ^ 0xFF

    def get_adc_messages(self):
        if self.AdcChannels == None:
            return []
        if self.AdcRate == None:
            return []
        return [f"{0x10:08x}{self.AdcChannels:02x}{self.AdcRate:02x}"]

    def recusb_011_adc(self, payload):
        ret = [{}] * 8
        payload = payload + "0" * 16  # pad to avoid errors
        channels, cc, cb, ca = (
            int(payload[:4], 16),
            int(payload[4:8], 16),
            int(payload[8:12], 16),
            int(payload[12:16], 16),
        )
        # this first msg defines which channels are in subsequent msgs
        self.adc_listinfirstmsg = [
            i for i in [7, 6, 5, 4, 3, 2, 1, 0] if (channels & (1 << (i)))
        ]
        thismsg = self.adc_listinfirstmsg[0:3]
        if thismsg is None:
            return None
        for ch, v in zip(thismsg, [cc, cb, ca]):
            if isinstance(ch, int):
                ret[ch] = {"measuredVoltage": v}
        path = "/adcInputController/adcInputs"
        return [{"path": path, "data": ret}]

    def recusb_111_adc(self, payload):
        ret = [{}] * 8
        payload = payload + "0" * 16  # pad to avoid errors
        cd, cc, cb, ca = (
            int(payload[:4], 16),
            int(payload[4:8], 16),
            int(payload[8:12], 16),
            int(payload[12:16], 16),
        )
        # this first msg defines which channels are in subsequent msgs
        thismsg = self.adc_listinfirstmsg[3:7]
        if thismsg is None:
            return None
        for ch, v in zip(thismsg, [cd, cc, cb, ca]):
            if isinstance(ch, int):
                ret[ch] = {"measuredVoltage": v}
        path = "/adcInputController/adcInputs"
        return [{"path": path, "data": ret}]

    def recusb_211_adc(self, payload):
        ret = [{}] * 8
        payload = payload + "0" * 16  # pad to avoid errors
        cd, cc, cb, ca = (
            int(payload[:4], 16),
            int(payload[4:8], 16),
            int(payload[8:12], 16),
            int(payload[12:16], 16),
        )
        # this first msg defines which channels are in subsequent msgs
        thismsg = self.adc_listinfirstmsg[7:]
        if thismsg is None:
            return None
        for ch, v in zip(thismsg, [cd, cc, cb, ca]):
            if isinstance(ch, int):
                ret[ch] = {"measuredVoltage": v}
        path = "/adcInputController/adcInputs"
        return [{"path": path, "data": ret}]
