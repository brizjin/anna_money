import os

from aiohttp import web

from web.server import index_handler, websocket_handler

routes = [
    web.get('/', index_handler),
    web.static('/static', os.path.join(os.path.dirname(__file__), 'static')),
    web.get('/ws', websocket_handler),
]
