import asyncio, json
import websockets
import aiohttp

async def connect(path):
    uri = f"ws://localhost:11111{path}"
    async with websockets.connect(uri) as websocket:
        rx = await websocket.recv()
        print(f"< {rx}")


async def fetch(session):
    cmd = ""
    print("starting...")
    async with session.get(f"http://localhost:36364/gizmogo") as resp:
        data = await resp.text()
        print(data)
    print(
        "example PATCH command: /relayController/relays/0/enabled = true\nexample GET command: relayController/relays"
    )
    while cmd != "quit":
        cmd = input("enter command ->")
        cmd.strip(" ")
        if cmd == "quit":
            continue
        if "=" in cmd:
            patch = True
            path, value = cmd.split("=")
            if value.isnumeric():
                value = int(value)
            elif value.upper() in ["TRUE", "FALSE"]:
                value = value.upper() == "TRUE"
        else:
            patch = False
            path = cmd
        if patch:
            async with session.patch(
                "http://localhost:36364",
                data=json.dumps({"op": "replace", "path": path, "value": value}).encode(
                    "utf-8"
                ),
            ) as resp:
                data = await resp.json()
                print(json.dumps(data, indent=2))
        else:
            async with session.get(f"http://localhost:36364{path}") as resp:
                data = await resp.json()
                print(json.dumps(data, indent=2))


async def go():
    async with aiohttp.ClientSession() as session:
        await fetch(session)


loop = asyncio.get_event_loop()
loop.run_until_complete(go())
loop.close()
