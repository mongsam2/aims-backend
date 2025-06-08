from rest_framework import serializers
from .models import Essay, EssayEvaluationScore

class EssayRequestSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=8)
    student_name = serializers.CharField(max_length=10)
    department = serializers.CharField(max_length=20)
    application_type = serializers.CharField(max_length=10)
    ocr_text = serializers.CharField()
    file = serializers.CharField()
    evaluation_category_id = serializers.IntegerField()


class EssayDetailSerializer(serializers.ModelSerializer):

    class EssayEvaluationScoreSerializer(serializers.ModelSerializer):
        evaluation_id = serializers.IntegerField(source="id")
        content = serializers.CharField(source="question.content")

        class Meta:
            model = EssayEvaluationScore
            fields = ("evaluation_id", "content", "score")

    evaluation_questions = serializers.SerializerMethodField()

    def get_evaluation_questions(self, obj):
        scores = obj.evaluation_scores.all()
        return self.EssayEvaluationScoreSerializer(scores, many=True).data

    class Meta:
        model = Essay
        fields = (
            "file",
            "summary",
            "score_by_length",
            "evaluation_questions",
        )


class EssayPatchSerializer(serializers.Serializer):
    evaluation_id = serializers.IntegerField()
    score = serializers.IntegerField()