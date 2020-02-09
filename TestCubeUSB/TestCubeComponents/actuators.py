class ActCurMessage:
    def __init__(self):
        self.actmonitorRate = None
        self.actmonitorChannels = None
        self.actmonitorThreshold = None

    def setPwmCurrentMonitorUpdateRate(self, rate: int):
        self.actmonitorRate = rate

    def setPwmFaultThreshold(self, Threshold: int):
        self.actmonitorThreshold = Threshold

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
