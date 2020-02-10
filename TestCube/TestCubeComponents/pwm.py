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

    def sethiconf(self, idx: int, activehi: bool):
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
        for i in range(6):
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
