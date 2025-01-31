from django.contrib import admin
from .models import StudentRecord, Summarization
from common.admin import CommonAdmin

# Register your models here.
@admin.register(StudentRecord)
class StudentRecordAdmin(CommonAdmin):
    pass