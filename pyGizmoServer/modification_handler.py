import jsonpatch, json
import copy, logging
import asyncio
from pyGizmoServer.utility import *
from aiohttp import web


class ModificationHandler:
    def __init__(self, controller, model=None):
        self.controller = controller
        self.schema = controller.schema
        self.logger = logging.getLogger("gizmoLogger")
        self.logger.debug("init")
        self.model = model

    async def handle_patch_from_client(self, request):
        request = json.loads(await request.text())
        self.logger.debug(f"{request}")
        if not isinstance(request, list):
            request = [request]
        response = []
        for r in request:
            path = r.get("path")
            if path is None:
                raise ValueError(f"no path provided in request: {r}")
            data = Utility.parse_path_against_schema_and_model(
                self.model, self.schema, path, read_write="w"
            )
            if data["error"] is not None:
                self.logger.error(f"{data['error']}")
                return web.json_response({"error": data["error"]})
            value = r.get("value")
            if value is not None:
                data["args"].append(value)
            # call the specified function with the associated parameters
            try:
                getattr(self.controller, data["routine"])(*data["args"])
            except Exception as e:
                self.logger.debug(f"{e}")
                data["error"] = f"bad request: {r}"
                return web.json_response(data)
            r["path"] = data["path_string"]
            response.append({"path": data["path_string"], "data": value})
        self.controller.finished()
        """
        create and apply the requested PATCH to the model
        """
        patch = jsonpatch.JsonPatch(request)
        jsonpatch.apply_patch(self.model, patch, in_place=True)
        return web.json_response(response)
