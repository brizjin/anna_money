import asyncio
import random
import string

import aiohttp_jinja2
from aiohttp import web, WSMessage


def generate_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


msg = generate_string(10)


@aiohttp_jinja2.template('index.jinja2')
async def index_handler(request):
    return dict(value=msg)


async def send_msg(app):
    global msg
    while True:
        await asyncio.sleep(1)
        if len(app['websockets']) > 0:
            msg = generate_string(10)
            for ws in app['websockets']:
                await ws.send_str(msg)


async def start_workers(app):
    asyncio.ensure_future(send_msg(app))


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].append(ws)

    try:
        async for msg in ws:  # type: WSMessage
            if msg.data == 'connect':
                pass
    except Exception as e:
        print(e.__dict__)
    finally:
        request.app['websockets'].remove(ws)
    return ws
