from rest_framework.views import APIView
from . import serializers
from .models import Essay, EssayEvaluationCategory
from students.models import Student
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from utils.upstage import call_upstage_llm
from utils.essay import get_length_penalty

class EssaysView(APIView):
    def get(self, request):
        essays = Essay.objects.values_list("id", flat=True)
        return Response(essays, status=200)

    def post(self, request):
        serializer = serializers.EssayRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            student = Student.objects.get_or_create(
                student_id=data["student_id"],
                student_name=data["student_name"],
                department=data["department"],
                application_type=data["application_type"],
            )

            evaluation_category = get_object_or_404(
                EssayEvaluationCategory, id=data["evaluation_category_id"]
            )

            refine_text = call_upstage_llm("refine_prompt.txt", data["ocr_text"])
            total_length = len(refine_text)
            length_penalty = get_length_penalty(evaluation_category.range_score, total_length)
            summary = call_upstage_llm("essay_prompt2.txt", data["ocr_text"])

            Essay.objects.create(
                ocr_text=data["ocr_text"],
                file=data["file"],
                summary=summary,
                score_by_length=length_penalty,
                category=evaluation_category,
                student=student,   
            )

            return Response("논술 답안지 업로드 성공", status=201)
        else:
            return Response(serializer.errors, status=400)