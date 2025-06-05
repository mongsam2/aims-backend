from rest_framework.views import APIView
from . import serializers
from students.models import Student
from .models import StudentRecord, StudentRecordEvaluationCategory
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class StudentRecordsView(APIView):

    def post(self, request):
        serializer = serializers.StudentRecordRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            student = Student.objects.get_or_create(
                student_id=data["student_id"],
                student_name=data["student_name"],
                department=data["department"],
                application_type=data["application_type"],
            )

            evaluation_category = get_object_or_404(
                StudentRecordEvaluationCategory, id=data["evaluation_category_id"]
            )

            student_record = StudentRecord(
                ocr_text=data["ocr_text"],
                file=data["file"],
                evaluation_category=evaluation_category,
                student=student,
            )

            return Response("생활기록부 업로드 성공", status=200)
        else:
            return Response(serializer.errors, status=400)
