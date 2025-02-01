from django.contrib import admin
from .models import Student, Department, ApplicantType

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'department', 'applicant_type')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ApplicantType)
class ApplicantTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)