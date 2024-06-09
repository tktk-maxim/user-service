from typing import List

from fastapi import APIRouter

from crud import get_all_entity, update_entity, delete_entity, create_entity, get_entity
from models import Event
from schemas import EventIn, EventCreate


router = APIRouter(
    tags=["Event"]
)


@router.post("/create/", response_model=EventIn)
async def create_event(event: EventCreate):
    event_obj = await create_entity(pydantic_model_class=EventCreate,
                                    tortoise_model_class=Event, entity=event)
    return event_obj


@router.get("/all/", response_model=List[EventIn])
async def get_events():
    events = await get_all_entity(tortoise_model_class=Event)
    return events


@router.get("/{event_id}", response_model=EventIn)
async def get_event(event_id: int):
    event = await get_entity(tortoise_model_class=Event, entity_id=event_id)
    return event


@router.put("/{event_id}", response_model=EventIn)
async def update_event_view(event_id: int, event: EventCreate):
    event_obj = await update_entity(pydantic_model_class=EventCreate, tortoise_model_class=Event,
                                    entity=event, entity_id=event_id)
    return await event_obj


@router.delete("/{event_id}", response_model=dict)
async def delete_event_view(event_id: int):
    return await delete_entity(tortoise_model_class=Event, entity_id=event_id)
