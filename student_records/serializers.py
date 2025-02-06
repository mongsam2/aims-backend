from rest_framework.serializers import ModelSerializer
from .models import StudentRecord, Summarization

class StudentRecordsSerializer(ModelSerializer):
    class Meta:
        model = StudentRecord
        fields = ("id", "file",)

class SummarizationSerializer(ModelSerializer):
    class Meta:
        model = Summarization
        exclude = ("id",)

class StudentRecordDetailSerializer(ModelSerializer):
    summarization = SummarizationSerializer()
    class Meta:
        model = StudentRecord
        fields = "__all__"

class StudentRecordMemoSerializer(ModelSerializer):
    class Meta:
        model = StudentRecord
        fields = ("memo",)

class StudentRecordScoreSerializer(ModelSerializer):
    class Meta:
        model = StudentRecord
        fields = ("score1", "score2", "score3", "score4",)