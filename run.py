from aiohttp import web

from web.app import create_app

web.run_app(create_app())
