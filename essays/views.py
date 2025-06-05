from rest_framework.views import APIView
from . import serializers
from .models import Essay, EssayEvaluationCategory, EssayEvaluationScore
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
        

class EssayDetailView(APIView):
    def get(self, request, student_record_id):
        essay = get_object_or_404(Essay, id=student_record_id)
        serializer = serializers.EssayDetailSerializer(essay)
        return Response(serializer.data, status=200)

    def patch(self, request, student_record_id):
        serializer = serializers.EssayPatchSerializer(data=request.data, many=True)
        if serializer.is_valid():
            data = serializer.validated_data
            essay = get_object_or_404(Essay, id=student_record_id)

            for evaluation in data:
                score_instance = get_object_or_404(
                    EssayEvaluationScore, id=evaluation["evaluation_id"]
                )
                score_instance.score = evaluation["score"]
                score_instance.save()

        else:
            return Response(serializer.errors, status=400)