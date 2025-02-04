from rest_framework.serializers import ModelSerializer
from .models import Document, DocumentPassFail

class DocumentPassFailSerializer(ModelSerializer):
    class Meta:
        model = DocumentPassFail
        exclude = ('document',)

class DocumentSerializer(ModelSerializer):
    document_pass_fails = DocumentPassFailSerializer(many=True)

    class Meta:
        model = Document
        fields = ('state', 'file', 'document_pass_fails')