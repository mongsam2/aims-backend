from django.contrib import admin
from .models import DocumentType

# Register your models here.
@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)  
