class DiMessage:
    def __init__(self):
        self.dimonitorrate = None

    def setDiMonitorUpdateRate(self, rate: int):
        self.dimonitorrate = int(rate / 50)

    def get_di_messages(self):
        if self.dimonitorrate == None:
            return []
        return [f"{0xa:08x}{self.dimonitorrate:02x}"]

    def recusb_b_digitalinputs(self, payload):
        d = []
        high = int(payload[:4], 16)
        data = [
            {"high": True} if (high & (1 << x)) else {"high": False} for x in range(12)
        ]
        path = "/digitalInputController/digitalInputs"
        d.append({"path": path, "data": data})
        return d
