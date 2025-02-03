from django.db import models

# Create your models here.
class Student(models.Model):
    '''
    대학에 지원한 학생들의 정보를 저장하는 모델
    '''
    id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    applicant_type = models.ForeignKey('ApplicantType', on_delete=models.CASCADE)
    required_documents = models.ManyToManyField('common.DocumentType')

    def __str__(self):
        return f"{self.id} {self.name}"

class Department(models.Model):
    '''
    대학에 있는 학과들의 정보를 담은 모델
    '''
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ApplicantType(models.Model):
    '''
    대학 지원 유형들의 정보를 담은 모델
    '''
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name