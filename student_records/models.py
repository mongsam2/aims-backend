from django.db import models
from common.models import CommonDocument

# Create your models here.
class StudentRecord(CommonDocument):
    '''
    학생생활기록부를 저장하는 모델
    '''
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name="student_records")
    summarization = models.OneToOneField('Summarization', on_delete=models.SET_NULL, null=True, blank=True, related_name='student_record')
    score1 = models.IntegerField(default=None, null=True, blank=True)
    score2 = models.IntegerField(default=None, null=True, blank=True)
    score3 = models.IntegerField(default=None, null=True, blank=True)
    score4 = models.IntegerField(default=None, null=True, blank=True)

class Summarization(models.Model):
    '''
    생기부에서 LLM으로 요약문과 질문을 추출해 저장하는 모델
    '''
    content = models.TextField()
    question = models.TextField()

    def __str__(self):
        return f"{self.id}의 생기부 요약문"