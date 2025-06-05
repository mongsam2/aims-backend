from django.db import models


# Manager
class StudentRecordEvaluationScoreManager(models.Manager):
    def get_queryset(self):
        return self.get_queryset().select_related("question")


# Create your models here.
class StudentRecordEvaluationCategory(models.Model):
    category_name = models.CharField(max_length=100)


class StudentRecordEvaluationQuestion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(
        StudentRecordEvaluationCategory,
        on_delete=models.CASCADE,
        db_column="category_id",
    )


class StudentRecord(models.Model):
    state = models.CharField(max_length=3, default="제출")
    uploaded_date = models.DateField(auto_now_add=True)
    ocr_text = models.TextField(null=True)
    file = models.TextField()
    memo = models.TextField(null=True)
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

    objects = StudentRecordEvaluationScoreManager()
