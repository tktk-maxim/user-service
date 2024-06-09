from datetime import date
from typing import List

from pydantic import BaseModel, EmailStr, Field

class SubdivisionCreate(BaseModel):
    name: str = Field(..., max_length=255)


class SubdivisionIn(SubdivisionCreate):
    id: int

class EventCreate(BaseModel):
    begin: date = None
    end: date = None
    description: str
class EmployeeCreate(BaseModel):
    full_name: str
    login: str
    password: str
    subdivision_id: int
    email: EmailStr | None = Field(default=None)
    leader: bool | None = Field(default=False, null=True)


class EmployeeIn(EmployeeCreate):
    id: int


class EmployeeCard(BaseModel):
    employee: EmployeeCreate
    events: EventCreate | None = Field(default=None, null=True)









class EventIn(EventCreate):
    id: int
