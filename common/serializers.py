from rest_framework.serializers import Serializer, CharField, ModelSerializer
from .models import DocumentType

class CommonDocumentSerializer(Serializer):
    document_type = CharField(max_length=50, read_only=True)
    status = CharField(max_length=9, read_only=True)

class DocumentTypesSerializer(ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'name',)