from datetime import date

from pydantic import BaseModel, EmailStr, Field


class SubdivisionCreate(BaseModel):
    name: str


class SubdivisionIn(SubdivisionCreate):
    id: int


class EventCreate(BaseModel):
    begin: date = None
    end: date = None
    description: str
    employee_id: int


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = Field(default=None, null=True)
    login: str
    password: str
    subdivision_id: int
    email: EmailStr | None = Field(default="example@gmail.com")
    leader: bool | None = Field(default=False, null=True)


class EmployeeIn(EmployeeCreate):
    id: int


class EmployeeCard(BaseModel):
    employee: EmployeeCreate
    events: EventCreate | None = Field(default=None, null=True)


class EventIn(EventCreate):
    id: int
