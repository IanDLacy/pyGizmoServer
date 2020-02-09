class RelayMessage:
    def __init__(self):
        self.RelayStates = [None] * 6

    def setRelay(self, relay: int, state: bool):
        self.RelayStates[relay] = state

    def get_relay_messages(self):
        if self.RelayStates == [None] * 6:
            return []
        mask = 0
        val = 0
        for i in range(0, len(self.RelayStates)):
            if self.RelayStates[i] != None:
                mask |= 1 << i
                if self.RelayStates[i]:
                    val |= 1 << i
        return [f"{0x12:08x}{mask:02x}{val:02x}"]
