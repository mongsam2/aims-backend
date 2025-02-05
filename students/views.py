# Views
from rest_framework.generics import ListAPIView

# Models
from students.models import Student
from documents.models import Document
from student_records.models import StudentRecord
from common.models import DocumentType

# Serializers
from .serializers import StudentListSerializer
from documents.serializers import DocumentSerializer

# Exceptions
from rest_framework.exceptions import NotAcceptable

# Create your views here.
class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer

class StudentDocumentsView(ListAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        document_type_name = self.kwargs['document_type']
        student_id = self.kwargs['id']
        if document_type_name == '학생생활기록부':
            raise NotAcceptable('학생생활기록부는 별도의 API로 요청해주세요.')
        elif document_type_name == '논술':
            raise NotAcceptable('논술은 별도의 API로 요청해주세요.')
        else:
            return Document.objects.filter(student=student_id, document_type__name=document_type_name).order_by('-upload_date')