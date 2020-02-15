import asyncio, json
import websockets
import aiohttp

try:
    import readline
except:
    print("readline not available - basic CLI")


async def connect(path, session):
    uri = f"ws://localhost:11111{path}"
    async with websockets.connect(uri) as websocket:
        path = "/wsinvoke"
        value = True
        async with session.patch(
            "http://localhost:36364",
            data=json.dumps({"op": "replace", "path": path, "value": value}).encode(
                "utf-8"
            ),
        ) as resp:
            data = await resp.json()
        rx = await websocket.recv()
        print(f"< {rx}")


def printhelp():
    for line in [
        "\nPATCH:\t\t/relayController/relays/0/enabled=true",
        "GET:\t\t/pwmController",
        "WebSock:\twsinvoke",
        "Quit:\t\tquit",
    ]:
        print(line)


async def fetch(session):
    cmd = ""
    print("starting...")
    printhelp()
    while cmd != "quit":
        ws = False
        cmd = input("\nenter command -> ")
        cmd.strip(" ")
        if cmd.lower() in ["help", "h", "-h", "--help"]:
            printhelp()
            continue
        elif cmd == "quit":
            continue
        elif cmd == "wsinvoke":
            await connect("/wsinvoke", session)
            ws = True
            path = "/wsinvoke"
            value = True
            patch = True
        elif "=" in cmd:
            patch = True
            path, value = cmd.split("=")
            if value.isnumeric():
                value = int(value)
            elif value.upper() in ["TRUE", "FALSE"]:
                value = value.upper() == "TRUE"
        else:
            patch = False
            path = cmd
        if path[0] != "/":
            path = "/" + path
        try:
            if patch:
                async with session.patch(
                    "http://localhost:36364",
                    data=json.dumps(
                        {"op": "replace", "path": path, "value": value}
                    ).encode("utf-8"),
                ) as resp:
                    data = await resp.json()
                    if not ws:
                        print(json.dumps(data, indent=2))
            else:
                async with session.get(f"http://localhost:36364{path}") as resp:
                    data = await resp.json()
                    print(json.dumps(data, indent=2))
        except:
            print("invalid command")


async def go():
    async with aiohttp.ClientSession() as session:
        await fetch(session)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())
    loop.close()


if __name__ == "__main__":
    main()
