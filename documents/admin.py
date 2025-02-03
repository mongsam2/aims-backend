from django.contrib import admin
from common.admin import CommonAdmin
from .models import Document, DocumentPassFail

# Register your models here.
@admin.register(Document)
class DocumentAdmin(CommonAdmin):
    pass