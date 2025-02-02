from rest_framework.serializers import ModelSerializer
from .models import StudentRecord
from students.models import Student

class StudentRecordsSerializer(ModelSerializer):
    class Meta:
        model = StudentRecord
        fields = ("id", "file",)

class StudentRecordDetailSerializer(ModelSerializer):
    class Meta:
        model = StudentRecord
        fields = "__all__"