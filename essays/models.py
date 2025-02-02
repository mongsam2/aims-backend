from django.db import models
from common.models import CommonDocument

# Create your models here.
class Essay(CommonDocument):
    '''
    논술 답안지를 저장하는 모델
    '''
    evaluation = models.TextField(null=True, blank=True)
    score_by_length = models.IntegerField(null=True, blank=True)
    criteria = models.ForeignKey('EssayCriteria', on_delete=models.SET_NULL, null=True, blank=True)


class EssayScore(models.Model):
    '''
    논술 답안지의 평가 항목별 점수를 저장하는 모델
    '''
    criteria_item = models.ForeignKey('CriteriaItem', on_delete=models.SET_NULL, null=True, blank=True, related_name='essay_scores')
    essay = models.ForeignKey('Essay', on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField()

    def __str__(self):
        return f"{self.essay.student}의 평가 항목 점수"


class EssayCriteria(models.Model):
    '''
    논술의 평가 항목과 글자 수 범위에 따른 패널티를 저장하는 모델
    '''
    title = models.CharField(max_length=100, null=True, blank=True)
    ranges = models.ManyToManyField('EssayRange')

    def __str__(self):
        return f"{self.title}"


class CriteriaItem(models.Model):
    '''
    논술 평가 기준별, 평가 항목들을 저장하는 모델
    '''
    content = models.TextField()
    essay_criteria = models.ForeignKey('EssayCriteria', on_delete=models.CASCADE, related_name='criteria_items')

    def __str__(self):
        return f"{self.content}"


class EssayRange(models.Model):
    '''
    논술의 글자 수 범위에 따른른 패널티를 저장하는 모델
    '''
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    penalty = models.IntegerField()

    def __str__(self):
        return f"{self.min_value} ~ {self.max_value} 글자: ({self.penalty}점)"