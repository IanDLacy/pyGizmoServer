import logging
from itertools import zip_longest
import dpath.util
from pyGizmoServer.subscription_server import SubscriptionServer
from pyGizmoServer.utility import Utility
from aiohttp import web
from aiojobs.aiohttp import spawn


def merge(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        d = dict(a)
        d.update({k: merge(a.get(k, "NADA"), b[k]) for k in b})
        return d

    if isinstance(a, list) and isinstance(b, list):
        return [merge(x, y) for x, y in zip_longest(a, b)]

    return a if b == "NADA" else b


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
        if not self.controller.running:
            await spawn(request, self.controller.usbrxhandler())
        path = request.path
        if path == "/model":
            path = "/"
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f"{path}")
        data = Utility.parse_path_against_schema_and_model(
            self.model, self.schema, path, read_write="r"
        )
        if data["error"] is not None:
            response = data["error"]
            self.logger.error(f"{response}")
        elif data.get("routine") is not None:
            res = await getattr(self.controller, data["routine"])(*data["args"])
            response = res
        else:
            response = {"path": data["path_string"], "data": data["model_data"]}
        return web.json_response(response)

    def handle_updates(self, updates):
        if not isinstance(updates, list):
            updates = [updates]
        for update in updates:
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug(f"{update['path']}")
            data = update.get("data")
            path = update.get("path")
            if isinstance(update, str) or data is None or path is None:
                self.logger.error("path or data key not found")
                continue
            location = dpath.util.get(self.model, path)
            dpath.util.set(self.model, path, merge(location, data))
            self.subscription_server.publish(
                {"path": path, "value": dpath.util.get(self.model, path)}
            )
