import asyncio
import sys
import time
import importlib
import logging
import os
import jinja2
import aiohttp_jinja2
import pkg_resources
from pyGizmoServer.modification_handler import ModificationHandler
from pyGizmoServer.query_handler import QueryHandler
from pyGizmoServer.utility import Utility
from aiohttp import web
from aiojobs.aiohttp import setup, spawn, atomic
from app_settings import AppSettings
from functools import partial, partialmethod

os.environ["TEST_ENV"] = "usb"
cfg = AppSettings(env_name="TEST_ENV")
starttime = time.strftime("%Y-%m-%d %H:%M")

""" get version from setup.py """
version = pkg_resources.require("pyGizmoServer")[0].version

""" setup logging """
logging.USB = 15
logging.addLevelName(logging.USB, "USB")
logging.Logger.usb = partialmethod(logging.Logger.log, logging.USB)
logging.usb = partial(logging.log, logging.USB)
gizmo_logger = logging.getLogger("gizmo_logger")
gizmo_logger.setLevel(getattr(logging, cfg.logging.file.loglevel))
formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
filehandler = logging.FileHandler(filename=cfg.logging.file.filename, mode="w")
filehandler.setLevel(getattr(logging, cfg.logging.file.loglevel))
filehandler.setFormatter(formatter)
consolehandler = logging.StreamHandler(sys.stdout)
consolehandler.setLevel(getattr(logging, cfg.logging.console.loglevel))
consolehandler.setFormatter(formatter)
gizmo_logger.addHandler(filehandler)
gizmo_logger.addHandler(consolehandler)
gizmo_logger.propogate = False
gizmo_logger.usb("usb")
gizmo_logger.debug("debug")
gizmo_logger.info("info")

""" setup controller """
controller = getattr(
    importlib.import_module(f"{cfg.controller}.{cfg.controller}"), cfg.controller
)()

""" set initial model """
model = Utility.initialize_model_from_schema(controller.schema)

""" setup modification, query handlers """
modification_handler = ModificationHandler(controller, model=model)
query_handler = QueryHandler(cfg.ws.ip, cfg.ws.port, controller, model=model)
controller.setcallback(query_handler.handle_updates)

coro_running = False


@aiohttp_jinja2.template("index.html")
async def get_index(request):
    return {
        "title": cfg.controller,
        "version": version,
        "time_started": starttime,
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
