# export TEST_ENV='development'

from pyGizmoServer.modification_handler import ModificationHandler
from pyGizmoServer.query_handler import QueryHandler
from pyGizmoServer.utility import Utility
from tests.mock_variables import MockVars
import sys, asyncio, sys, time, json, textwrap, importlib
from aiohttp import web
from aiojobs.aiohttp import setup, spawn, atomic
import time, jinja2, aiohttp_jinja2, logging, aiojobs, pkg_resources
from app_settings import AppSettings

cfg = AppSettings()


""" get version from setup.py """
version = pkg_resources.require("pyGizmoServer")[0].version

""" setup logging """
logger = logging.getLogger("gizmoLogger")
logger.setLevel(getattr(logging, cfg.logging.loglevel))
handler = logging.FileHandler(filename=cfg.logging.filename, mode="w")
handler.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
logger.addHandler(handler)

""" get schema """
with open(f"schemas/{cfg.controller.schema}") as f:
    hwschema = json.load(f)

""" set initial model """
model = Utility.initialize_model_from_schema(f"schemas/{cfg.model.schema}")

""" setup modification, query handlers """
modification_handler = ModificationHandler(hwschema, model=model)
query_handler = QueryHandler(cfg.ws.ip, cfg.ws.port, hwschema, model=model)

""" setup controller """
controller = getattr(
    importlib.import_module(f"controllers.{cfg.controller.name}"), cfg.controller.name
)(query_handler.handle_updates)

coro_running = False


@aiohttp_jinja2.template("index.html")
async def get_index(request):
    return {
        "title": cfg.controller.name,
        "version": version,
        "time_started": time.strftime("%Y-%m-%d %H:%M"),
        "Request_Host": request.host,
        "Request_Path": request.path,
        "Request_QueryString": request.query_string,
    }


@atomic
async def start_your_engines(request):
    global coro_running
    if not coro_running:
        await spawn(request, controller.usbrxhandler())
        coro_running = True
    return web.Response(text="VROOM")


def get_model(request):
    return query_handler.handle_get(request)


def make_app():
    controller.start()
    modification_handler.add_controller(controller)
    query_handler.add_controller(controller)

    app = web.Application(loop=asyncio.get_event_loop())
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(["templates", "static"]))
    app["static_root_url"] = "/static"
    app.router.add_get("/", get_index)
    app.router.add_static("/static", "static")
    app.router.add_get("/gizmogo", start_your_engines)
    app.router.add_get("/model", get_model)
    app.router.add_route("GET", r"/{tail:.*}", query_handler.handle_get)
    app.router.add_route(
        "PATCH", r"/{tail:.*}", modification_handler.handle_patch_from_client
    )
    setup(app)
    return app


def main():
    try:
        print(time.asctime(), f"Server started - {cfg.tcp.ip}:{cfg.tcp.port}")
        web.run_app(make_app(), host=cfg.tcp.ip, port=cfg.tcp.port)
    except KeyboardInterrupt:
        sys.exit()
