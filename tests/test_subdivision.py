from httpx import AsyncClient
import pytest


@pytest.mark.anyio
async def test_positive_create_subdivision(client: AsyncClient) -> None:
    response = await client.post("/subdivision/create/", json={"name": "developers"})
    assert response.status_code == 200
    assert response.json()["name"] == "developers"


@pytest.mark.anyio
async def test_positive_update_subdivision(client: AsyncClient) -> None:
    response = await client.get("/subdivision/all/")
    subdivision_id = response.json()[-1]["id"]
    response = await client.put(f"/subdivision/{subdivision_id}", json={"name": "workers"})
    assert response.status_code == 200, response.text
    assert response.json() == {"id": subdivision_id, "name": "workers"}


@pytest.mark.anyio
async def test_positive_get_subdivisions(client: AsyncClient) -> None:
    response = await client.get("/subdivision/all/")
    assert response.status_code == 200
    data = response.json()
    assert data != []


@pytest.mark.anyio
async def test_negative_get_subdivision(client: AsyncClient) -> None:
    response = await client.get(f"/subdivision/{-1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Entity obj with id: -1 not found"


@pytest.mark.anyio
async def test_positive_get_subdivision(client: AsyncClient) -> None:
    response = await client.get("/subdivision/all/")
    subdivision_id = response.json()[-1]["id"]
    response = await client.get(f"/subdivision/{subdivision_id}")
    assert response.status_code == 200
    assert response.json()["name"] is not None


@pytest.mark.anyio
async def test_positive_delete_subdivision(client: AsyncClient) -> None:
    response = await client.get("/subdivision/all/")
    subdivision_id = response.json()[-1]["id"]
    response = await client.delete(f"/subdivision/{subdivision_id}")
    assert response.json()["deleted"] is True


@pytest.mark.anyio
async def test_negative_delete_subdivision(client: AsyncClient) -> None:
    response = await client.delete(f"/subdivision/{-1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Entity obj with id: -1 not found"
