import pytest
from hamcrest import has_length, equal_to, matches_regexp, greater_than
from hamcrest.core import assert_that
from lxml.html import html5parser

from web.app import create_app
from web.server import generate_string

value_matcher = matches_regexp(r'^(\w|\d){10}$')


def test_random_string():
    n = 2
    assert_that(generate_string(n), has_length(n))


@pytest.fixture
def client(loop, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(create_app()))


async def test_hello_world(client):
    response = await client.get('/')
    assert_that(response.status, equal_to(200))
    text = await response.text()
    value = html5parser.fromstring(text).xpath('.//*[@id="value"]/text()').pop()

    assert_that(value, value_matcher)


async def test_static(client):
    response = await client.get('/static/main.js')
    assert_that(response.status, equal_to(200))
    assert_that(await response.text(), has_length(greater_than(0)))


async def test_ws(client):
    async with client.ws_connect('/ws') as ws:
        await ws.send_str('connect')
        r = await ws.receive()
        assert_that((await ws.receive()).data, value_matcher)
        assert_that((await ws.receive()).data, value_matcher)
