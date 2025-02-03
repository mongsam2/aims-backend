from django.db import models
from common.models import CommonDocument

# Create your models here.
class Document(CommonDocument):
    '''
    입시 제출 서류들을 저장하는 모델
    '''
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='documents')

class DocumentPassFail(models.Model):
    '''
    제출 서류의 부적합 이유들을 저장하는 모델
    '''
    page = models.IntegerField()
    failed_condition = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='document_pass_fails')