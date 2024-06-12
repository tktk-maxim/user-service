import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_positive_create_event(client: AsyncClient) -> None:
    subdivision = await client.post("/subdivision/create/", json={"name": "developers"})
    employee = await client.post("/employee/create/", json={
      "first_name": "TestFN",
      "last_name": "TestLN",
      "middle_name": "TestMN",
      "login": "t_log",
      "password": "t_pass",
      "subdivision_id": subdivision.json()["id"],
      "email": "user@example.com",
      "leader": False
    })
    response = await client.post("/event/create/", json={
      "begin": "2024-06-09",
      "end": "2024-06-09",
      "description": "HB",
      "employee_id": employee.json()["id"]
    })
    assert response.status_code == 200
    assert response.json()["description"] == "HB"


@pytest.mark.anyio
async def test_negative_create_event(client: AsyncClient) -> None:
    response = await client.get("/employee/all/")
    assert response.status_code == 200

    response = await client.post("/event/create/", json={
      "begin": "2024-06-09",
      "end": "2024-06-12",
      "description": "HB",
      "employee_id": response.json()[-1]["id"]
    })

    assert response.status_code == 422
    assert response.json()["detail"] == "Intersection with another event (check the list of events and try again)"


@pytest.mark.anyio
async def test_positive_update_event(client: AsyncClient) -> None:
    response = await client.get("/event/all/")
    assert response.status_code == 200
    event_id = response.json()[-1]["id"]
    response = await client.put(f"/event/{event_id}", json={
      "begin": "2024-06-09",
      "end": "2024-06-09",
      "employee_id": response.json()[-1]["employee_id"],
      "description": "day off"})
    assert response.status_code == 200
    assert response.json()["description"] == "day off"


@pytest.mark.anyio
async def test_positive_get_event(client: AsyncClient) -> None:
    response = await client.get("/event/all/")
    assert response.status_code == 200
    event_id = response.json()[-1]["id"]
    response = await client.get(f"/event/{event_id}")
    assert response.json()["description"] == "day off"


@pytest.mark.anyio
async def test_negative_get_event(client: AsyncClient) -> None:
    response = await client.get(f"/event/{-1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event obj with id: -1 not found"


@pytest.mark.anyio
async def test_positive_delete_event(client: AsyncClient) -> None:
    response = await client.get("/event/all/")
    event_id = response.json()[-1]["id"]
    response = await client.delete(f"/event/{event_id}")
    assert response.json()["deleted"] is True
