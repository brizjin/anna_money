import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from web.routes import routes
from web.server import start_workers


def create_app():
    app = web.Application()
    app.add_routes(routes)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    app['static_root_url'] = '/static'

    app['websockets'] = []
    app.on_startup.append(start_workers)

    return app
