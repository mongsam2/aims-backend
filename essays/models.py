from django.db import models
from common.models import CommonDocument

# Create your models here.
class Essay(CommonDocument):
    '''
    논술 답안지를 저장하는 모델
    '''
    evaluation = models.OneToOneField('Evaluation', on_delete=models.SET_NULL, null=True, blank=True)
    criteria = models.ForeignKey('EssayCriteria', on_delete=models.SET_NULL, null=True, blank=True)


class Evaluation(models.Model):
    content = models.TextField()


class EssayCriteria(models.Model):
    '''
    논술의 평가 항목과 글자 수 범위에 따른 패널티를 저장하는 모델
    '''
    content = models.TextField()
    ranges = models.ManyToManyField('EssayRange')
    year = models.IntegerField()

    def __str__(self):
        return f"{self.year}년도 논술 평가항목"


class EssayRange(models.Model):
    '''
    논술의 글자 수 범위에 따른른 패널티를 저장하는 모델
    '''
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    penalty = models.IntegerField()

    def __str__(self):
        return f"{self.min} ~ {self.max} 글자: ({self.penalty}점)"