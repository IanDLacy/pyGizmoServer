class ActCurMessage:
    def __init__(self):
        self.actmonitorRate = None
        self.actmonitorChannels = 0x0FFF
        self.actmonitorThreshold = 60

    def setPwmCurrentMonitorUpdateRate(self, rate: int):
        rate = int(rate / 50)
        self.actmonitorRate = rate

    def setPwmFaultThreshold(self, threshold: int):
        threshold = int(threshold / 50)
        self.actmonitorThreshold = threshold

    #    def setPwmFaultDelay(self):

    def setPwmCurrentMonitorChannels(self, channelMask: int):
        self.actmonitorChannels = channelMask

    def get_actcur_messages(self):
        if self.actmonitorChannels == None:
            return []
        if self.actmonitorRate == None:
            return []
        if self.actmonitorThreshold == None:
            return []
        return [
            f"{0xc:08x}{self.actmonitorChannels:04x}{self.actmonitorRate:02x}{self.actmonitorThreshold:02x}"
        ]

    def recusb_1d_actfault(self, payload):
        _, faults = (int(payload[:1], 16), int(payload[1:4], 16))
        data = [
            {"currentMonitor": {"faulty": True}}
            if (faults & (1 << x))
            else {"currentMonitor": {"faulty": False}}
            for x in range(12)
        ]

        path = "/pwmController/pwms"
        return [{"path": path, "data": data}]

    def recusb_00d_actcurrent(self, payload):
        ret = [{}] * 12
        payload = payload + "0" * 16  # pad to avoid errors
        channels, cc, cb, ca = (
            int(payload[:4], 16),
            int(payload[4:8], 16),
            int(payload[8:12], 16),
            int(payload[12:16], 16),
        )
        # this first msg defines which channels are in subsequent msgs
        self.actcurrent_listinfirstmsg = [
            i for i in [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0] if (channels & (1 << (i)))
        ]
        thismsg = self.actcurrent_listinfirstmsg[0:3]
        if thismsg is None:
            return None
        for ch, v in zip(thismsg, [cc, cb, ca]):
            if isinstance(ch, int):
                ret[ch] = {"currentMonitor": {"measuredCurrent": v}}
        path = "/pwmController/pwms"
        return [{"path": path, "data": ret}]

    def recusb_10d_actcurrent(self, payload):
        ret = [{}] * 12
        payload = payload + "0" * 16  # pad to avoid errors
        cd, cc, cb, ca = (
            int(payload[:4], 16),
            int(payload[4:8], 16),
            int(payload[8:12], 16),
            int(payload[12:16], 16),
        )
        thismsg = self.actcurrent_listinfirstmsg[3:7]
        if thismsg is None:
            return None
        for ch, v in zip(thismsg, [cd, cc, cb, ca]):
            if isinstance(ch, int):
                ret[ch] = {"currentMonitor": {"measuredCurrent": v}}
        path = "/pwmController/pwms"
        return [{"path": path, "data": ret}]

    def recusb_20d_actcurrent(self, payload):
        ret = [{}] * 12
        payload = payload + "0" * 16  # pad to avoid errors
        cd, cc, cb, ca = (
            int(payload[:4], 16),
            int(payload[4:8], 16),
            int(payload[8:12], 16),
            int(payload[12:16], 16),
        )
        thismsg = self.actcurrent_listinfirstmsg[7:11]
        if thismsg is None:
            return None
        for ch, v in zip(thismsg, [cd, cc, cb, ca]):
            if isinstance(ch, int):
                ret[ch] = {"currentMonitor": {"measuredCurrent": v}}
        path = "/pwmController/pwms"
        return [{"path": path, "data": ret}]

    def recusb_30d_actcurrent(self, payload):
        ret = [{}] * 12
        payload = payload + "0" * 16  # pad to avoid errors
        cd = (int(payload[:4], 16),)
        thismsg = self.actcurrent_listinfirstmsg[12:]

        if thismsg is None:
            return None
        for ch, v in zip(thismsg, [cd]):
            if isinstance(ch, int):
                ret[ch] = {"currentMonitor": {"measuredCurrent": v}}
        path = "/pwmController/pwms"
        return [{"path": path, "data": ret}]
