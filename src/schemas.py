from datetime import date
from typing import List

from pydantic import BaseModel, EmailStr, Field, field_validator


class SubdivisionCreate(BaseModel):
    name: str


class SubdivisionIn(SubdivisionCreate):
    id: int


class EventCreate(BaseModel):
    begin: date
    end: date
    description: str
    employee_id: int


class EventIn(EventCreate):
    id: int


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = Field(default=None, null=True)
    login: str
    password: str
    subdivision_id: int
    email: EmailStr | None = Field(default="example@gmail.com")
    leader: bool | None = Field(default=False, null=True)
    chat_id: int | None = Field(default=0, null=True)
    telegram_name: str

    @field_validator('first_name', 'last_name', 'login')
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError('Field cannot be empty')
        return value


class EmployeeIn(EmployeeCreate):
    id: int


class EventForCard(BaseModel):
    begin: date
    end: date
    description: str


class EmployeeCard(BaseModel):
    employee: EmployeeCreate
    events: List[EventForCard]


class Auth(BaseModel):
    login: str
    password: str


class EmployeeParams(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    login: str | None = None
    password: str | None = None
    subdivision_id: int | None = None
    email: EmailStr | None = None
    chat_id: str | None = None
    telegram_name: str | None = None

