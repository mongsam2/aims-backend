from rest_framework.serializers import ModelSerializer
from .models import Essay

class EssaysSerializer(ModelSerializer):
    class Meta:
        model = Essay
        fields = ('id', 'file', 'criteria')