from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from .models import Essay, CriteriaItem, EssayCriteria, EssayScore

class EssaysSerializer(ModelSerializer):
    class Meta:
        model = Essay
        fields = ('id', 'file', 'criteria')

class CriteriaItemSerializer(ModelSerializer):
    '''
    context에 essay_id가 전달되어야 함
    '''
    score = SerializerMethodField()

    class Meta:
        model = CriteriaItem
        fields = ('id', 'content', 'score')

    def get_score(self, obj):
        essay_id = self.context['essay_id']
        try:
            score = obj.essay_scores.get(essay_id=essay_id).score
            return score
        except EssayScore.DoesNotExist:
            return None

class EssayCriteriaSerializer(ModelSerializer):
    criteria_items = CriteriaItemSerializer(many=True)

    class Meta:
        model = EssayCriteria
        fields = ('title', 'criteria_items')

class EssayCriteriaListSerializer(ModelSerializer):

    class Meta:
        model = EssayCriteria
        fields = ('id', 'title')

class EssayDetailSerializer(ModelSerializer):
    criteria = EssayCriteriaSerializer()

    class Meta:
        model = Essay
        fields = '__all__'

class EssayScoreSerializer(ModelSerializer):
    class Meta:
        model = EssayScore
        fields = ('score', 'criteria_item')

    def validate_criteria_item(self, criteria_item):
        '''
        해당 평가 항목이 해당 논술의 평가 항목인지 검증
        '''
        essay = self.context['essay']
        if criteria_item.id not in  essay.criteria.criteria_items.values_list('id', flat=True):
            raise ValidationError(f"CriteriaItem [{criteria_item}] 은 해당 논술의 평가 항목이 아닙니다.")
        return criteria_item