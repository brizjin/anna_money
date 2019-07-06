import asyncio
import random
import string

import aiohttp_jinja2
from aiohttp import web, WSMessage


def generate_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


@aiohttp_jinja2.template('index.jinja2')
async def index_handler(request):
    return dict(value=generate_string(10))


async def send_msg(app):
    while True:
        msg = generate_string(10)
        for ws in app['websockets']:
            # print(f'send msg')
            await ws.send_str(msg)
        await asyncio.sleep(1)


async def start_workers(app):
    asyncio.ensure_future(send_msg(app))


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].append(ws)

    try:
        async for msg in ws:  # type: WSMessage
            if msg.data == 'connect':
                # await ws.send_str("connected")
                # print('connected')
                pass
    except Exception as e:
        print(e.__dict__)
    finally:
        request.app['websockets'].remove(ws)
    # print('websocket_handler exit')
    return ws
