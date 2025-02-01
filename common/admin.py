from django.contrib import admin
from .models import DocumentType

# Register your models here.
class CommonAdmin(admin.ModelAdmin):
    list_display = ('student', 'document_type', 'state', 'upload_date')



@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)  
