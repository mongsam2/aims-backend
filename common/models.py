from django.db import models
from students.models import Student

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

class DocumentType(models.Model):
    '''
    서류의 종류를 저장하는 모델 (학생생활기록부, 논술, 기타 등등)
    '''
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name

class CommonDocument(models.Model):
    '''
    StudentRecord, Essay, Document 모델에 공통으로 사용할 필드를 정의한 추상 모델
    '''
    extraction = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=upload_to)
    state = models.CharField(max_length=10, choices=StateChoices.choices, default=StateChoices.검토)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True)
    memo = models.TextField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.document_type} ({self.state})"  

    class Meta:
        abstract = True