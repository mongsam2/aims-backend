from django.db import models

# Create your models here.
def upload_to(instance, filename):
    '''
    FileField의 upload_to 매개변수에 사용할 함수
    '''
    return f"{instance.student}/{instance.document_type}/{filename}"

class StateChoices(models.TextChoices):
    '''
    서류의 제출 상태 (제출, 검토)
    '''
    제출 = ('제출', '제출')
    검토 = ('검토', '검토')

class CommonDocument(models.Model):
    '''
    StudentRecord, Essay, Document 모델에 공통으로 사용할 필드를 정의한 추상 모델
    '''
    extraction = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=upload_to)
    state = models.CharField(max_length=10, choices=StateChoices.choices, default=StateChoices.검토)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    document_type = models.ForeignKey('DocumentType', on_delete=models.SET_NULL, null=True)
    memo = models.TextField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True