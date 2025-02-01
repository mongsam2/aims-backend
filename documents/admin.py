from django.contrib import admin
from common.admin import CommonAdmin
from .models import Document, DocumentFail

# Register your models here.

class DocumentAdmin(CommonAdmin):
    pass