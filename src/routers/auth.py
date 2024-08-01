from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from crud import create_entity, get_all_entity, get_employee_card, delete_entity, update_entity, search_employee
from crud import checking_id_for_existence, get_auth_entity
from schemas import EmployeeIn, EmployeeCreate, EmployeeCard, Auth
from models import Employee, Subdivision


router = APIRouter(
    tags=["Auth"]
)


class Status(BaseModel):
    message: str


@router.post("/entity/", response_model=Optional[EmployeeIn])
async def get_auth_view(data: Auth):
    return await get_auth_entity(Employee, data.login, data.password)

