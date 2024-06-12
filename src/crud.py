from fastapi import HTTPException
from typing import List, TypeVar, Type, Dict

from pydantic import BaseModel
from tortoise import Model
from tortoise.exceptions import DoesNotExist

from models import Employee, Event

AnyPydanticModel = TypeVar('AnyPydanticModel', bound=BaseModel)
AnyTortoiseModel = TypeVar('AnyTortoiseModel', bound=Model)


async def checking_id_for_existence(tortoise_model_class: Type[AnyTortoiseModel], entity_id: int):
    try:
        await tortoise_model_class.get(id=entity_id)
    except DoesNotExist:
        raise HTTPException(status_code=404,
                            detail=f"{tortoise_model_class.__name__} obj with id: {entity_id} not found")


async def validation_date(event_data: AnyPydanticModel, event_id=-1):
    await checking_id_for_existence(Employee, event_data.employee_id)

    if event_data.begin > event_data.end:
        raise HTTPException(status_code=422, detail=f'Date entered incorrectly (value begin > end)')

    events = await Event.filter(employee_id=event_data.employee_id)
    for event in events:
        if (event.id != event_id) and ((event_data.begin <= event.begin <= event_data.end) or (event.end >= event_data.begin >= event.begin)):
            raise HTTPException(status_code=422,
                                detail=f'Intersection with another event (check the list of events and try again)')


async def create_entity(tortoise_model_class: Type[AnyTortoiseModel],
                        entity: AnyPydanticModel) -> AnyTortoiseModel:
    entity_obj = await tortoise_model_class.create(**entity.dict())
    return entity_obj


async def update_entity(tortoise_model_class: Type[AnyTortoiseModel],
                        entity_id: int, entity: AnyPydanticModel) -> AnyTortoiseModel:
    await checking_id_for_existence(tortoise_model_class, entity_id)

    await tortoise_model_class.filter(id=entity_id).update(**entity.dict())
    entity_obj = await tortoise_model_class.get(id=entity_id)
    return entity_obj


async def get_all_entity(tortoise_model_class: Type[AnyTortoiseModel]) -> List[AnyTortoiseModel]:
    return await tortoise_model_class.all()


async def get_entity(tortoise_model_class: Type[AnyTortoiseModel], entity_id: int) -> AnyTortoiseModel:
    await checking_id_for_existence(tortoise_model_class, entity_id)
    return await tortoise_model_class.get(id=entity_id)


async def delete_entity(tortoise_model_class: Type[AnyTortoiseModel], entity_id: int):
    await checking_id_for_existence(tortoise_model_class, entity_id)
    deleted = await tortoise_model_class.filter(id=entity_id).delete()
    if not deleted:
        raise HTTPException(status_code=404,
                            detail=f"{tortoise_model_class.__name__} obj with id: {entity_id} not found")
    return {"deleted": True}


async def get_employee_card(employee_id: int) -> Dict:
    await checking_id_for_existence(Employee, employee_id)
    return {'employee': await Employee.get(id=employee_id),
            'events': await Event.filter(employee_id=employee_id).order_by('begin')}


async def search_employee(employee_data: str) -> List[Employee]:
    if ' ' in employee_data:
        data = employee_data.split()
        print(data, len(data))
        return await Employee.filter(last_name=data[0], first_name=data[1],
                                     middle_name=data[2] if len(data) == 3 else "")
    elif '@' in employee_data:
        return await Employee.filter(email=employee_data)
    return await Employee.filter(login=employee_data)
