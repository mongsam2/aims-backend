from rest_framework.serializers import ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField
from .models import Document, DocumentPassFail
from students.models import Student

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
        fields = ('id', 'state', 'file', 'document_pass_fails')

class DocumentDetailSerializer(ModelSerializer):
    document_type = SerializerMethodField()

    class Meta:
        model = Document
        fields = ("id", "document_type", "state", "file", "student")
    
    def get_document_type(self, document):
        return document.document_type.name

class DocumentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "document_type", "state", "file", "student")