from django.db import models
from common.models import CommonDocument

# Create your models here.
class StudentRecord(CommonDocument):
    summarization = models.OneToOneField('Summarization', on_delete=models.SET_NULL, null=True, blank=True, related_name='student_record')

class Summarization(models.Model):
    content = models.TextField()
    question = models.TextField()

    def __str__(self):
        return f"{self.student_record.student}의 생기부 요약문"