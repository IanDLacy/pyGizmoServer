class PwmMessage:
    def __init__(self):
        self.Freq = [None] * 2
        self.Hiconf = [None] * 12

        self.PwmEnabled = [None] * 12
        self.Duty = [None] * 12

    def setPwmFrequencyA(self, hz: int):
        self.Freq[0] = hz

    def setPwmFrequencyB(self, hz: int):
        self.Freq[1] = hz

    def sethiconf(self, idx: int, activehi: str):
        if activehi.upper() == "HIGH":
            activehi = True
        elif activehi.upper() == "LOW":
            activehi = False
        else:
            raise ValueError("active configuration must be either high or low")
        self.Hiconf[idx] = activehi

    def setPwmDutyCycle(self, idx: int, duty: int):
        self.Duty[idx] = duty

    def setPwmEnabled(self, idx: int, enabled: bool):
        self.PwmEnabled[idx] = enabled

    def getUsbMsg8(self):
        if self.PwmEnabled == [None] * 12:
            return []
        mask = 0
        val = 0
        for i in range(0, len(self.PwmEnabled)):
            if self.PwmEnabled[i] != None:
                mask |= 1 << i
                if self.PwmEnabled[i]:
                    val |= 1 << i
        return [f"{8:08x}{mask:04x}{val:04x}"]

    def getUsbMsg6(self, bank: int):
        if self.Duty[bank * 6 : bank * 6 + 6] == ([None] * 6):
            return []

        dutymask = 0
        for i in range(6):
            if self.Duty[i + bank * 6] != None:
                dutymask |= 1 << i
        r = f"{6:08x}{bank:02x}{dutymask:02x}"
        for i in reversed(range(6)):
            r += f"{self.Duty[i+bank*6] or 0:02x}"
        return [r]

    def getUsbMsg4(self):
        if (self.Freq == [None] * 2) and (self.Hiconf == [None] * 12):
            return []
        freqmask = 0x0
        hilomask = 0x000
        hiloval = 0x000
        for i in range(0, len(self.Freq)):
            if self.Freq[i] != None:
                freqmask |= 8 >> i

        for i in range(0, len(self.Hiconf)):
            if self.Hiconf[i] != None:
                hilomask |= 1 << i
                if self.Hiconf[i]:
                    hiloval |= 1 << i

        try:
            assert freqmask <= 0xF
            assert hilomask <= 0xFFF
            assert hiloval <= 0xFFF
        except:
            raise ValueError("PwmMessageFieldOverflow")

        r = "{:08x}{:01x}{:03x}0{:03x}{:04x}{:04x}".format(
            0x04, freqmask, hilomask, hiloval, self.Freq[0] or 0, self.Freq[1] or 0
        )
        return [r]

    def get_pwm_messages(self):
        return (
            self.getUsbMsg4()
            + self.getUsbMsg6(0)
            + self.getUsbMsg6(1)
            + self.getUsbMsg8()
        )

    def recusb_5_pwmfreq(self, payload):
        acthi, freqa, freqb = payload[:4], payload[4:8], payload[8:12]
        d = []
        path = "/pwmController/bankA/frequency"
        data = int(freqa, 16)
        d.append({"path": path, "data": data})
        path = "/pwmController/bankB/frequency"
        data = int(freqb, 16)
        d.append({"path": path, "data": data})
        path = "/pwmController/pwms"
        data = [
            {"activeConfiguration": "high"}
            if (int(acthi, 16) & (1 << x))
            else {"activeConfiguration": "low"}
            for x in range(12)
        ]
        d.append({"path": path, "data": data})
        return d

    def recusb_7_pwmdutycycle(self, payload):
        ret = [{}] * 12
        bank, _, dcf, dce, dcd, dcc, dcb, dca = (
            int(payload[:2], 16),
            int(payload[2:4], 16),
            int(payload[4:6], 16),
            int(payload[6:8], 16),
            int(payload[8:10], 16),
            int(payload[10:12], 16),
            int(payload[12:14], 16),
            int(payload[14:16], 16),
        )
        ret[6 * bank + 0] = {"dutyCycle": dca}
        ret[6 * bank + 1] = {"dutyCycle": dcb}
        ret[6 * bank + 2] = {"dutyCycle": dcc}
        ret[6 * bank + 3] = {"dutyCycle": dcd}
        ret[6 * bank + 4] = {"dutyCycle": dce}
        ret[6 * bank + 5] = {"dutyCycle": dcf}
        path = "/pwmController/pwms"
        return [{"path": path, "data": ret}]

    def recusb_9_pwmenable(self, payload):
        d = []
        enabled = int(payload[:4], 16)
        data = [
            {"enabled": True} if (enabled & (1 << x)) else {"enabled": False}
            for x in range(12)
        ]
        path = "/pwmController/pwms"
        d.append({"path": path, "data": data})
        return d
