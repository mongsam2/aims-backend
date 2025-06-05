from rest_framework import serializers
from .models import StudentRecord, StudentRecordEvaluationScore


class StudentRecordRequestSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=8)
    student_name = serializers.CharField(max_length=10)
    department = serializers.CharField(max_length=20)
    application_type = serializers.CharField(max_length=10)
    ocr_text = serializers.CharField()
    file = serializers.CharField()
    evaluation_category_id = serializers.IntegerField()


class StudentRecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRecord
        fields = ("id",)


class StudentRecordDetailSerializer(serializers.ModelSerializer):

    class StudentRecordEvaluationScoreSerializer(serializers.ModelSerializer):
        evaluation_id = serializers.IntegerField(source="id")
        title = serializers.CharField(source="question.title")
        description = serializers.CharField(source="question.description")

        class Meta:
            model = StudentRecordEvaluationScore
            fields = ("evaluation_id", "title", "description", "score")

    evaluation_questions = StudentRecordEvaluationScoreSerializer(many=True)

    class Meta:
        model = StudentRecord
        fields = (
            "file",
            "memo",
            "summary",
            "interview_questions",
            "evaluation_questions",
        )


class StudentRecordPatchSerializer(serializers.Serializer):

    class StudentRecordEvaluationScoreSerializer(serializers.Serializer):
        evaluation_id = serializers.IntegerField()
        score = serializers.IntegerField()

    memo = serializers.CharField()
    evaluations = StudentRecordEvaluationScoreSerializer(many=True)
