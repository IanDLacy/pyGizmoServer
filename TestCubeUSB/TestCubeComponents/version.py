class VersionMessage:
    def __init__(self):
        self.ask = None
        pass

    async def getFirmwareVersion(self):
        data = await self.wait_for_version()
        path = '/version'
        return [{'path': path, 'data': data}]

    def get_version_messages(self):
        if self.ask == None:
            return []
        return [f"{0x40:08x}"]
