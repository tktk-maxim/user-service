# mypy: no-disallow-untyped-decorators
# pylint: disable=E0611,E0401

from httpx import AsyncClient


from src.models import Users

import pytest


@pytest.mark.anyio
async def test_create_user(client: AsyncClient) -> None:
    # nosec
    response = await client.post("/users", json={"username": "adminneee"})
    assert response.status_code == 200, response.text
    data = response.json()
    print(data["username"])
    assert data["username"] == "adminneee"
    assert "id" in data
    user_id = data["id"]

    user_obj = await Users.get(id=user_id)
    assert user_obj.id == user_id

