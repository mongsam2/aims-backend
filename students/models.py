from django.db import models


class StudentManager(models.Manager):
    def get_or_create(
        self, student_id: str, student_name: str, department: str, application_type: str
    ):
        try:
            return self.get(
                code=student_id,
                department=department,
                application_type=application_type,
            )
        except:
            return self.create(
                code=student_id,
                name=student_name,
                department=department,
                application_type=application_type,
            )


# Create your models here.
class Student(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=10)
    department = models.CharField(max_length=20)
    application_type = models.CharField(max_length=10)

    objects = StudentManager()

    class Meta:
        db_table = "student"
