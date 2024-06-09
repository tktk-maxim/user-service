from fastapi import Depends
from typing import List, Annotated

from fastapi import APIRouter
from pydantic import BaseModel

from crud import create_entity, get_all_entity, get_employee_card, delete_entity, update_entity, search_employee
from schemas import EmployeeIn, EmployeeCreate, EmployeeCard
from models import Employee


router = APIRouter(
    tags=["Employee"]
)


class Status(BaseModel):
    message: str


@router.post("/create/", response_model=EmployeeIn)
async def create_employee_view(employee: EmployeeCreate):
    employee_obj = await create_entity(pydantic_model_class=EmployeeCreate,
                                       tortoise_model_class=Employee, entity=employee)
    return employee_obj


@router.get("/all/", response_model=List[EmployeeIn])
async def get_employees_view():
    employees = await get_all_entity(tortoise_model_class=Employee)
    return employees


@router.get("/card/{employee_id}", response_model=EmployeeCard)
async def get_card_employee_view(employee_id: int):
    employee_card_obj = await get_employee_card(employee_id)
    return employee_card_obj


@router.put("/{employee_id}", response_model=EmployeeIn)
async def update_employee_view(employee_id: int, employee: EmployeeCreate):
    employee_obj = await update_entity(pydantic_model_class=EmployeeCreate,
                                       tortoise_model_class=Employee, entity=employee, entity_id=employee_id)
    return await employee_obj


@router.delete("/{employee_id}", response_model=dict)
async def delete_employee_view(employee_id: int):
    return await delete_entity(tortoise_model_class=Employee, entity_id=employee_id)


@router.get("/search/", response_model=List[EmployeeIn])
async def search_employee_view(employee_data: str):
    return await search_employee(employee_data)
