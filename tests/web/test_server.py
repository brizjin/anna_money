import pytest
from hamcrest import has_length, equal_to, matches_regexp
from hamcrest.core import assert_that

from web import server
from web.server import generate_string


def test_random_string():
    n = 2
    assert_that(generate_string(n), has_length(n))


@pytest.fixture
def client(loop, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(server.app))


async def test_hello_world(client):
    response = await client.get('/')
    assert_that(response.status, equal_to(200))
    assert_that(await response.text(), matches_regexp(r'^(\w|\d){10}$'))
