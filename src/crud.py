from fastapi import HTTPException, Depends
from typing import List, TypeVar, Type, Dict, Annotated

from pydantic import BaseModel
from tortoise import Model
from tortoise.exceptions import DoesNotExist
from tortoise.queryset import QuerySetSingle, QuerySet

from models import Employee, Subdivision
from schemas import EventCreate, EmployeeCreate, SubdivisionCreate, EmployeeCard

AnyPydanticModel = TypeVar('AnyPydanticModel', bound=BaseModel)
AnyTortoiseModel = TypeVar('AnyTortoiseModel', bound=Model)


async def create_entity(pydantic_model_class: Type[AnyPydanticModel], tortoise_model_class: Type[AnyTortoiseModel],
                        entity: AnyPydanticModel) -> AnyTortoiseModel:
    entity_obj = await tortoise_model_class.create(**entity.dict())
    return entity_obj


async def update_entity(pydantic_model_class: Type[AnyPydanticModel], tortoise_model_class: Type[AnyTortoiseModel],
                        entity_id: int, entity: AnyPydanticModel) -> AnyTortoiseModel:
    try:
        await tortoise_model_class.filter(id=entity_id).update(**entity.dict())
        entity_obj = await tortoise_model_class.get(id=entity_id)
        return entity_obj
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Entity obj with id: {entity_id} not found")


async def get_all_entity(tortoise_model_class: Type[AnyTortoiseModel]) -> List[AnyTortoiseModel]:
    return await tortoise_model_class.all()


async def get_entity(tortoise_model_class: Type[AnyTortoiseModel], entity_id: int) -> AnyTortoiseModel:
    return await tortoise_model_class.get(id=entity_id)


async def delete_entity(tortoise_model_class: Type[AnyTortoiseModel], entity_id: int):
    try:
        deleted = await tortoise_model_class.filter(id=entity_id).delete()
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Entity obj with id: {entity_id} not found")
        return {"deleted": True}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Entity obj with id: {entity_id} not found")


async def get_employee_card(employee_id: int) -> Dict:
    try:
        return {'employee': await Employee.get(id=employee_id), 'events': None}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Employee not found")


async def search_employee(employee_data: str) -> List[Employee]:
    if ' ' in employee_data:
        return await Employee.filter(full_name=employee_data)
    elif '@' in employee_data:
        return await Employee.filter(email=employee_data)
    return await Employee.filter(login=employee_data)
