from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise
from config import get_db_url, settings

from routers.employees import router as router_employee
from routers.events import router as router_event
from routers.subdivisions import router as router_subdivision
from routers.auth import router as router_auth


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    print(f"Connecting DB {get_db_url(settings.run_test)}")

    async with RegisterTortoise(
        application,
        db_url=get_db_url(settings.run_test),
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

app.include_router(
    router=router_auth,
    prefix="/auth",
    tags=["Auth"]
)
