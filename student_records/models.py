from django.db import models


# Manager
class StudentRecordEvaluationScoreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("question")


# Create your models here.
class StudentRecordEvaluationCategory(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        db_table = "student_record_evaluation_category"


class StudentRecordEvaluationQuestion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(
        StudentRecordEvaluationCategory,
        on_delete=models.CASCADE,
        db_column="category_id",
        related_name="evaluation_questions"
    )

    class Meta:
        db_table = "student_record_evaluation_question"


class StudentRecord(models.Model):
    state = models.CharField(max_length=3, default="제출")
    uploaded_date = models.DateField(auto_now_add=True)
    ocr_text = models.TextField(null=True)
    file = models.TextField()
    memo = models.TextField(default="")
    summary = models.TextField(null=True)
    interview_questions = models.TextField(null=True)
    evaluation_category = models.ForeignKey(
        StudentRecordEvaluationCategory,
        on_delete=models.SET_NULL,
        null=True,
        db_column="evaluation_category_id",
    )
    student = models.ForeignKey(
        "students.Student", on_delete=models.CASCADE, db_column="student_id"
    )

    class Meta:
        db_table = "student_record"


class StudentRecordEvaluationScore(models.Model):
    score = models.PositiveIntegerField(null=True)
    student_record = models.ForeignKey(
        StudentRecord, on_delete=models.CASCADE, db_column="student_record_id", related_name="evaluation_scores"
    )
    question = models.ForeignKey(
        StudentRecordEvaluationQuestion,
        on_delete=models.CASCADE,
        db_column="question_id",
    )

    objects = StudentRecordEvaluationScoreManager()

    class Meta:
        db_table = "student_record_evaluation_score"
