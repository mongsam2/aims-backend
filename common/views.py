from rest_framework.generics import ListAPIView
from students.serializers import ApplicantTypesSerializer
from students.models import ApplicantType

# Create your views here.
class ApplicantTypesView(ListAPIView):
    queryset = ApplicantType.objects.all()
    serializer_class = ApplicantTypesSerializer