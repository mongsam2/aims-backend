from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Essay, CriteriaItem, EssayCriteria

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
        return obj.essay_scores.get(essay_id=essay_id).score

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