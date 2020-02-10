class DiMessage:
    def __init__(self):
        self.dimonitorrate = None

    def setDiMonitorUpdateRate(self, rate: int):
        self.dimonitorrate = rate

    def get_di_messages(self):
        if self.dimonitorrate == None:
            return []
        return [f"{0xa:08x}{self.dimonitorrate:02x}"]
