
import logging
class AdcMessage:
    def __init__(self):
        self.AdcChannels = 0x3F
        self.logger = logging.getLogger('gizmoLogger')
        self.AdcRate = None

    def setAdcMonitorUpdateRate(self, rate: int):
        self.logger.debug(f"{rate}")
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
