import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_positive_create_employee(client: AsyncClient) -> None:
    subdivision = await client.post("/subdivision/create/", json={"name": "developers"})
    response = await client.post("/employee/create/", json={
      "first_name": "Ivan",
      "last_name": "Ivanov",
      "middle_name": None,
      "login": "t_log",
      "password": "t_log",
      "subdivision_id": subdivision.json()["id"],
      "email": "user@example.com",
      "leader": True
    })
    assert response.status_code == 200
    assert response.json()["first_name"] == "Ivan"


@pytest.mark.anyio
async def test_negative_create_without_first_name(client: AsyncClient) -> None:
    response = await client.post("/employee/create/", json={
      "first_name": "",
      "last_name": "Ivanov",
      "middle_name": None,
      "login": "t_log",
      "password": "t_log",
      "subdivision_id": "str",
      "email": "user@example.com",
      "leader": True
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, Field cannot be empty"


@pytest.mark.anyio
async def test_negative_create_employee(client: AsyncClient) -> None:
    response = await client.post("/employee/create/", json={
      "first_name": "Ivan",
      "last_name": "Ivanov",
      "middle_name": None,
      "login": "t_log",
      "password": "t_log",
      "subdivision_id": "str",
      "email": "user@example.com",
      "leader": True
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == ("Input should be a valid integer, "
                                                   "unable to parse string as an integer")


@pytest.mark.anyio
async def test_positive_update_employee(client: AsyncClient) -> None:
    response = await client.get("/employee/all/")
    assert response.status_code == 200
    employee_id = response.json()[-1]["id"]
    response = await client.put(f"/employee/{employee_id}", json={
      "first_name": "Ivan",
      "last_name": "Ivanov",
      "middle_name": "Ivanovich",
      "login": "t_log",
      "password": "t_log",
      "subdivision_id": response.json()[-1]["subdivision_id"],
      "email": "user@example.com",
      "leader": True
    })
    assert response.status_code == 200
    assert response.json()["middle_name"] == "Ivanovich"


@pytest.mark.anyio
async def test_positive_get_employee(client: AsyncClient) -> None:
    response = await client.get("/employee/all/")
    assert response.status_code == 200
    employee_id = response.json()[-1]["id"]
    response = await client.get(f"/employee/card/{employee_id}")
    assert response.status_code == 200
    assert response.json()["employee"] is not None
    assert response.json()["events"] is not None


@pytest.mark.anyio
async def test_negative_get_employee(client: AsyncClient) -> None:
    response = await client.get(f"/employee/card/{-1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee obj with id: -1 not found"


@pytest.mark.anyio
async def test_positive_search_employee(client: AsyncClient) -> None:
    response = await client.get("/employee/all/")

    employee_login = response.json()[-1]["login"]
    employee_full_name = str(response.json()[-1]["last_name"]+' '+response.json()[-1]["first_name"] +
                             ' '+response.json()[-1]["middle_name"])
    employee_email = response.json()[-1]["email"]

    response = await client.get(f"/employee/search/?employee_data={employee_login}")
    assert response.status_code == 200
    assert response.json()[0]["login"] == employee_login

    response = await client.get(f"/employee/search/?employee_data={employee_full_name}")
    assert response.status_code == 200
    print(employee_full_name)
    print(response.json())
    assert response.json()[0]["first_name"] is not None

    response = await client.get(f"/employee/search/?employee_data={employee_email}")
    assert response.status_code == 200
    assert response.json()[0]["email"] == employee_email


@pytest.mark.anyio
async def test_negative_search_employee(client: AsyncClient) -> None:
    response = await client.get(f"/employee/search/?employee_data=negative@gmail.com")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_positive_delete_employee(client: AsyncClient) -> None:
    response = await client.get("/employee/all/")
    employee_id = response.json()[-1]["id"]
    response = await client.delete(f"/employee/{employee_id}")
    assert response.json()["deleted"] is True