import jsonpatch, json, itertools
from itertools import zip_longest
import copy, logging
import dpath.util
import io, copy, re, time, asyncio
from pyGizmoServer.subscription_server import SubscriptionServer
from pyGizmoServer.utility import Utility
from aiohttp import web


def merge(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        d = dict(a)
        d.update({k: merge(a.get(k, None), b[k]) for k in b})
        return d

    if isinstance(a, list) and isinstance(b, list):
        return [merge(x, y) for x, y in itertools.zip_longest(a, b)]

    return a if b is None else b


class QueryHandler:
    def __init__(self, ws_ip, ws_port, controller, model=None):
        self.controller = controller
        self.schema = controller.schema
        self.model = model
        self.err = None
        self.logger = logging.getLogger("gizmoLogger")
        self.logger.debug("init")
        self.subscription_server = SubscriptionServer(ws_ip, ws_port)
        self.subscribers = {}

    async def handle_get(self, request):
        path = request.path
        if path == "/model":
            path = "/"
        self.logger.debug(f"{path}")
        data = Utility.parse_path_against_schema_and_model(
            self.model, self.schema, path, read_write="r"
        )
        if data["error"] is not None:
            response = data["error"]
            self.logger.error(f"{response}")
            return
        if data.get("routine") is not None:
            getattr(self.controller, data["routine"])(
                *data["args"]
            )
            self.controller.finished()
            """TODO: this doesnt do anything right now"""
        return web.json_response(
            {"path": data["path_string"], "data": data["model_data"]}
        )

    async def handle_updates(self, updates):
        self.logger.debug(f"{updates}")
        outgoing = []
        if not isinstance(updates, list):
            updates = [updates]
        for update in updates:
            data = update.get("data")
            path = update.get("path")
            if isinstance(update, str) or data is None or path is None:
                self.logger.error("path or data key not found")
                continue
            location = dpath.util.get(self.model, path)
            dpath.util.set(self.model, merge(location, data), path)
            outgoing.append({"path": path, "value": data})
        await self.subscription_server.publish(outgoing)
