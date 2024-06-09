from tortoise.models import Model
from tortoise import fields


class Employee(Model):
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    middle_name = fields.CharField(max_length=255, default=None, null=True)
    login = fields.CharField(max_length=50)
    password = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100)
    subdivision = fields.ForeignKeyField('models.Subdivision', on_delete=fields.CASCADE)
    leader = fields.BooleanField(default=False, null=True)

    def __str__(self):
        return self.last_name


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
