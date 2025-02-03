# Views
from rest_framework.generics import ListAPIView

# Models
from students.models import Student
from documents.models import Document
from student_records.models import StudentRecord
from essays.models import Essay

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
        document_type = self.kwargs['document_type']
        student_id = self.kwargs['id']
        if document_type == '학생생활기록부':
            raise NotAcceptable('학생생활기록부는 별도의 API로 요청해주세요.')
        elif document_type == '논술':
            raise NotAcceptable('논술은 별도의 API로 요청해주세요.')
        else:
            return Document.objects.filter(student=self.kwargs['id'], document_type=self.kwargs['document_type']).order_by('-upload_date')