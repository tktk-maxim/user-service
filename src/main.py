from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from config import DATABASE_URL
from tortoise.contrib.fastapi import RegisterTortoise

from routers.employees import router as router_employee
from routers.events import router as router_event
from routers.subdivisions import router as router_subdivision


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print(f"Connecting to database at {DATABASE_URL}")

    async with RegisterTortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    ):
        yield


app = FastAPI(title="User service", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello world"}


app.include_router(
    router=router_employee,
    prefix="/employee",
    tags=["Employee"]
)

app.include_router(
    router=router_event,
    prefix="/event",
    tags=["Event"]
)

app.include_router(
    router=router_subdivision,
    prefix="/subdivision",
    tags=["Subdivision"]
)
