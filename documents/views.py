# Views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin

# Serializers
from .serializers import DocumentUploadSerializer, DocumentDetailSerializer

# Utils
from utils.upstage import execute_ocr
from utils.document import predict_document_type, assign_student_id_and_document_type
from django.conf import settings
import os

# Exceptions
from rest_framework.exceptions import ParseError, NotFound

from common.models import DocumentType
from students.models import Student
from .models import Document

# Create your views here.
class DocumentUploadView(GenericAPIView, CreateModelMixin):
    serializer_class = DocumentUploadSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save(state="검토")

        api_key = settings.UPSTAGE_API_KEY
        excuted_text, confidence = execute_ocr(api_key, document.file.file)
        document_type, confidence = predict_document_type(document.file.path)
        student_id, date, student_name = assign_student_id_and_document_type(excuted_text)

        try:
            default_student = Student.objects.get(name="무명이")
            default_document_type = DocumentType.objects.get(name="알수없음")
            document.student = default_student
            document.document_type = default_document_type
            document.extraction = excuted_text
            document.save()
        except Student.DoesNotExist:
            raise NotFound("'무명이'와 '해당없음' 이 존재하지 않습니다.")
        
        student_instance = Student.objects.filter(id=student_id).first()
        document_type_instance = DocumentType.objects.filter(name=document_type).first()
        if student_instance:
            document.student = student_instance
        if document_type_instance:
            document.document_type = document_type_instance
        if student_id != "20250000" and document_type != "해당없음":
            document.state = "제출"
        document.save()
        return Response({"student_name": student_name, "date": date}, status=201)
    
class DocumentUpdateView(UpdateAPIView):
    serializer_class = DocumentDetailSerializer
    queryset = Document.objects.all()
    lookup_field = 'id'
    http_method_names = ["patch"]