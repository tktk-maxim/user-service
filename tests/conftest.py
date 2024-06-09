import os
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"






@pytest.fixture(scope='session', autouse=True)
def set_test_database_url():
    load_dotenv()
    os.environ['PYTEST_RUNNING'] = 'true'
    print(f"PYTEST_RUNNING set to: {os.getenv('PYTEST_RUNNING')}")


@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c
