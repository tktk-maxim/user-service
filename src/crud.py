from fastapi import HTTPException
from typing import List, TypeVar, Type, Dict

from pydantic import BaseModel
from tortoise import Model
from tortoise.exceptions import DoesNotExist

from models import Employee

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
    try:
        return await tortoise_model_class.get(id=entity_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Entity obj with id: {entity_id} not found")


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
        data = employee_data.split()
        print(data, len(data))
        return await Employee.filter(first_name=data[0], last_name=data[1],
                                     middle_name=data[2] if len(data) == 3 else "")
    elif '@' in employee_data:
        return await Employee.filter(email=employee_data)
    return await Employee.filter(login=employee_data)
