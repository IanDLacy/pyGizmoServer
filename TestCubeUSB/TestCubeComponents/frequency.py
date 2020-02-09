class FrequencyMessage:
    def __init__(self):
        self.freqmonitorRate = None
        self.freqmonitorChannels = None

    def setFrequencyInputEnabled(self, freqmask: int):
        self.freqmonitorChannels = freqmask

    def setFrequencyMonitorRate(self, rate):
        self.freqmonitorRate = rate

    def get_freq_messages(self):
        if self.freqmonitorRate == None:
            return []
        if self.freqmonitorChannels == None:
            return []
        return [f"{0xe:08x}{self.freqmonitorChannels:02x}{self.freqmonitorRate:02x}"]
