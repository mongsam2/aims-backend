# Views
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin

# Serializers
from .serializers import DocumentUploadSerializer

# Utils
from utils.upstage import execute_ocr
from utils.document import predict_document_type
from django.conf import settings
import os

# Exceptions
from rest_framework.exceptions import ParseError

# Create your views here.
class DocumentUploadView(GenericAPIView, CreateModelMixin):
    serializer_class = DocumentUploadSerializer

    def post(self, request):
        file = request.data.get('file')
        if not file:
            raise ParseError("파일을 첨부해주세요.")
        
        api_key = settings.UPSTAGE_API_KEY
        excuted_text = execute_ocr(api_key, file.file)
        document_type = predict_document_type(file.file)
        return Response({"document_type": document_type})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()