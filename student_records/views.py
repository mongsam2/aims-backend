from rest_framework.views import APIView
from . import serializers
from students.models import Student
from .models import (
    StudentRecord,
    StudentRecordEvaluationCategory,
    StudentRecordEvaluationScore,
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from utils.upstage import call_upstage_llm


class StudentRecordsView(APIView):
    def get(self, request):
        student_records = StudentRecord.objects.values_list("id", flat=True)
        return Response(student_records, status=200)

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

            summary = call_upstage_llm("summarization.txt", data["ocr_text"])
            interview_questions = call_upstage_llm("question.txt", data["ocr_text"])

            student_record = StudentRecord.objects.create(
                ocr_text=data["ocr_text"],
                file=data["file"],
                summary=summary,
                interview_questions=interview_questions,
                evaluation_category=evaluation_category,
                student=student,
            )

            return Response("생활기록부 업로드 성공", status=201)
        else:
            return Response(serializer.errors, status=400)


class StudentRecordDetailView(APIView):
    def get(self, request, student_record_id):
        student_record = get_object_or_404(StudentRecord, id=student_record_id)
        serializer = serializers.StudentRecordDetailSerializer(student_record)
        return Response(serializer.data, status=200)

    def patch(self, request, student_record_id):
        serializer = serializers.StudentRecordPatchSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            student_record = get_object_or_404(StudentRecord, id=student_record_id)

            student_record.memo = data["memo"]
            student_record.save()

            for evaluation in data["evaluations"]:
                score_instance = get_object_or_404(
                    StudentRecordEvaluationScore, id=evaluation["evaluation_id"]
                )
                score_instance.score = evaluation["score"]
                score_instance.save()

        else:
            return Response(serializer.errors, status=400)


class StudentRecordEvaluationView(APIView):
    def get(self, request):
        categories = StudentRecordEvaluationCategory.objects.all()
        serializer = serializers.StudentRecordEvaluationCategorySerializer(
            categories, many=True
        )
        return Response(serializer.data, status=200)
