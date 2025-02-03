# Views
from rest_framework.generics import ListAPIView

# Models
from students.models import Student
from documents.models import Document
from common.models import CommonDocument, DocumentType

# Serializers
from .serializers import StudentListSerializer

# Create your views here.
class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer

        