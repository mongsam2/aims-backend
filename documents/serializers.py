from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Document, DocumentPassFail

class DocumentUploadSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ('file',)

class DocumentPassFailSerializer(ModelSerializer):
    class Meta:
        model = DocumentPassFail
        exclude = ('document',)

class DocumentSerializer(ModelSerializer):
    document_pass_fails = DocumentPassFailSerializer(many=True)

    class Meta:
        model = Document
        fields = ('state', 'file', 'document_pass_fails')

class DocumentDetailSerializer(ModelSerializer):
    document_type = SerializerMethodField()

    class Meta:
        model = Document
        fields = ("document_type", "state", "file")
    
    def get_document_type(self, document):
        return document.document_type.name