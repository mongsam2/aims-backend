from django.db import models


# Create your models here.
class Student(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=10)
    department = models.CharField(max_length=20)
    application_type = models.CharField(max_length=10)
