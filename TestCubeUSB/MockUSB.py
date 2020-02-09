import asyncio, json


class MockUSB:
    def __init__(self):
        self.callback = None
        self.msg = None
        with open("TestCube/schema.json") as f:
            self.schema = json.load(f)

    def setcallback(self, callback):
        if not callable(callback):
            raise ValueError("callback must be a function")
        self.callback = callback

    def start(self):
        if self.callback is None:
            raise RuntimeError('controller callback not set')
        pass

    def setRelay(self, relay, state):
        pass

    def finished(self):
        pass

    def wsinvoke(self, msg):
        print(f"wsinvoke: {msg}")
        if self.msg is None:
            self.msg = msg

    async def usbrxhandler(self):
        while 1:
            if self.msg is not None:
                print(f"handler: {self.msg}")
                await self.callback(self.msg)
                self.msg = None
            await asyncio.sleep(0.001)
