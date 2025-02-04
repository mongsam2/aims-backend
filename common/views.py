from rest_framework.generics import ListAPIView
from students.serializers import ApplicantTypesSerializer
from .serializers import DocumentTypesSerializer

from students.models import ApplicantType
from .models import DocumentType

# Create your views here.
class ApplicantTypesView(ListAPIView):
    queryset = ApplicantType.objects.all()
    serializer_class = ApplicantTypesSerializer

class DocumentTypesView(ListAPIView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypesSerializer