from rest_framework import serializers
from .models import (
    StudentRecord,
    StudentRecordEvaluationScore,
    StudentRecordEvaluationCategory,
)


class StudentRecordRequestSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=8)
    student_name = serializers.CharField(max_length=10)
    department = serializers.CharField(max_length=20)
    application_type = serializers.CharField(max_length=10)
    ocr_text = serializers.CharField()
    file = serializers.CharField()
    evaluation_category_id = serializers.IntegerField()


class StudentRecordDetailSerializer(serializers.ModelSerializer):

    class StudentRecordEvaluationScoreSerializer(serializers.ModelSerializer):
        evaluation_id = serializers.IntegerField(source="id")
        title = serializers.CharField(source="question.title")
        description = serializers.CharField(source="question.description")

        class Meta:
            model = StudentRecordEvaluationScore
            fields = ("evaluation_id", "title", "description", "score")
    evaluation_questions = serializers.SerializerMethodField()

    def get_evaluation_questions(self, obj):
        scores = obj.evaluation_scores.all()
        print(scores)
        return self.StudentRecordEvaluationScoreSerializer(scores, many=True).data

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

    memo = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    evaluations = StudentRecordEvaluationScoreSerializer(many=True, required=False)


class StudentRecordEvaluationCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentRecordEvaluationCategory
        fields = ("id", "category_name")
