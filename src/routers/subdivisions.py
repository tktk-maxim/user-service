from typing import List

from fastapi import APIRouter
from schemas import SubdivisionCreate, SubdivisionIn
from models import Subdivision
from crud import get_all_entity, update_entity, delete_entity, get_entity, create_entity


router = APIRouter(
    tags=["Subdivision"]
)


@router.post("/create/", response_model=SubdivisionIn)
async def create_subdivision(subdivision: SubdivisionCreate):
    subdivision_obj = await create_entity(tortoise_model_class=Subdivision, entity=subdivision)
    return subdivision_obj


@router.get("/all/", response_model=List[SubdivisionIn])
async def get_subdivisions():
    subdivisions = await get_all_entity(tortoise_model_class=Subdivision)
    return subdivisions


@router.get("/{subdivision_id}", response_model=SubdivisionIn)
async def get_subdivision(subdivision_id: int):
    subdivision = await get_entity(tortoise_model_class=Subdivision, entity_id=subdivision_id)
    return subdivision


@router.put("/{subdivision_id}", response_model=SubdivisionIn)
async def update_subdivision_view(subdivision_id: int, subdivision: SubdivisionCreate):
    subdivision_obj = await update_entity(tortoise_model_class=Subdivision, entity=subdivision,
                                          entity_id=subdivision_id)
    return await subdivision_obj


@router.delete("/{subdivision_id}", response_model=dict)
async def delete_subdivision_view(subdivision_id: int):
    return await delete_entity(tortoise_model_class=Subdivision, entity_id=subdivision_id)
