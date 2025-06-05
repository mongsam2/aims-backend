from django.db import models


# Create your models here.
class Document(models.Model):
    state = models.CharField(max_length=3)
    uploaded_date = models.DateField(auto_now_add=True)
    document_type = models.CharField(max_length=10, null=True)
    memo = models.TextField(null=True)
    student = models.ForeignKey(
        "students.Student", on_delete=models.CASCADE, db_column="student_id"
    )

    class Meta:
        db_table = "document"
