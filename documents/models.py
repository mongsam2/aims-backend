from django.db import models
from common.models import CommonDocument

# Create your models here.
def upload_to(instance, filename):
    '''
    FileField의 upload_to 매개변수에 사용할 함수
    '''
    return f"documents/{filename}"

class Document(CommonDocument):
    '''
    입시 제출 서류들을 저장하는 모델
    '''
    file = models.FileField(upload_to=upload_to)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)

class DocumentPassFail(models.Model):
    '''
    제출 서류의 부적합 이유들을 저장하는 모델
    '''
    page = models.IntegerField()
    failed_condition = models.CharField(max_length=200)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='document_pass_fails', null=True)