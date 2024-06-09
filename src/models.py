
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields


class Employee(Model):
    full_name = fields.CharField(max_length=255)
    login = fields.CharField(max_length=50)
    password = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100, null=True)
    subdivision = fields.ForeignKeyField('models.Subdivision', on_delete=fields.CASCADE)
    leader = fields.BooleanField(default=False, null=True)

    def __str__(self):
        return self.full_name


class Event(Model):
    employee = fields.ForeignKeyField('models.Employee', on_delete=fields.CASCADE)
    begin = fields.DateField()
    end = fields.DateField()
    description = fields.TextField()

    def __str__(self):
        return self.description


class Subdivision(Model):
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


Employee_pydantic = pydantic_model_creator(Employee, name="Employee")
Employee_pydantic_no_ids = pydantic_model_creator(Employee, name="EmployeeIn", exclude_readonly=True)

Subdivision_pydantic = pydantic_model_creator(Subdivision, name="Subdivision")
Subdivision_pydantic_no_ids = pydantic_model_creator(Subdivision, name="SubdivisionIn", exclude_readonly=True)

Event_pydantic = pydantic_model_creator(Event, name="Event")
Event_pydantic_no_ids = pydantic_model_creator(Event, name="EventIn", exclude_readonly=True)
