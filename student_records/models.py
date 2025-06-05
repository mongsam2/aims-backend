from django.db import models


class StudentRecordManager(models.Manager):
    def get_or_create(
        self, student_id: str, student_name: str, department: str, application_type: str
    ):
        try:
            return self.get(
                code=student_id,
                department=department,
                application_type=application_type,
            )
        except:
            return self.create(
                code=student_id,
                name=student_name,
                department=department,
                application_type=application_type,
            )


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
    state = models.CharField(max_length=3)
    uploaded_date = models.DateField(auto_now_add=True)
    ocr_text = models.TextField(null=True)
    file = models.URLField()
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


class StudentRecordEvaluationScore(models.Model):
    score = models.PositiveIntegerField(null=True)
    student_record = models.ForeignKey(
        StudentRecord, on_delete=models.CASCADE, db_column="student_record_id"
    )
    question = models.ForeignKey(
        StudentRecordEvaluationQuestion,
        on_delete=models.CASCADE,
        db_column="question_id",
    )
