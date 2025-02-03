# Views
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin

# Serializers
from .serializers import DocumentUploadSerializer

# Utils
from utils.upstage import execute_ocr

# Exceptions
from rest_framework.exceptions import ParseError

# Create your views here.
class DocumentUploadView(GenericAPIView, CreateModelMixin):
    serializer_class = DocumentUploadSerializer

    def post(self, request):
        file = request.data.get('file')
        if not file:
            raise ParseError("파일을 첨부해주세요.")
        excuted_text = execute_ocr(file.file)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()