from django.db import models


# Create your models here.
class EssayEvaluationCategory(models.Model):
    title = models.CharField(max_length=100)
    range_score = models.TextField()

    class Meta:
        db_table = "essay_evaluation_category"


class EssayEvaluationQuestion(models.Model):
    content = models.TextField()
    category = models.ForeignKey(
        EssayEvaluationCategory, on_delete=models.CASCADE, db_column="category_id", related_name="evaluation_questions"
    )

    class Meta:
        db_table = "essay_evaluation_question"


class Essay(models.Model):
    state = models.CharField(max_length=3)
    upload_date = models.DateField(auto_now_add=True)
    ocr_text = models.TextField(null=True)
    file = models.URLField()
    summary = models.TextField(null=True)
    score_by_length = models.IntegerField(null=True)
    category = models.ForeignKey(
        EssayEvaluationCategory,
        on_delete=models.SET_NULL,
        null=True,
        db_column="category_id",
    )
    student = models.ForeignKey(
        "students.Student", on_delete=models.CASCADE, db_column="student_id"
    )

    class Meta:
        db_table = "essay"


class EssayEvaluationScore(models.Model):
    score = models.PositiveIntegerField(null=True)
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE, db_column="essay_id", related_name="evaluation_scores")
    question = models.ForeignKey(
        EssayEvaluationQuestion, on_delete=models.CASCADE, db_column="question_id"
    )

    class Meta:
        db_table = "essay_evaluation_score"
