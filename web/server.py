import random
import string

from aiohttp import web


def generate_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


async def handle(request):
    return web.Response(text=generate_string(10))


app = web.Application()
app.add_routes([web.get('/', handle), ])
