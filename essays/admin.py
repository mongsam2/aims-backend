from django.contrib import admin
from common.admin import CommonAdmin
from .models import Essay, EssayScore, EssayCriteria, CriteriaItem, EssayRange

# Register your models here.
@admin.register(Essay)
class EssayAdmin(CommonAdmin):
    pass

@admin.register(EssayScore)
class EssayScoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'criteria_item', 'score')

@admin.register(EssayCriteria)
class EssayCriteriaAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

@admin.register(CriteriaItem)
class CriteriaItemAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

@admin.register(EssayRange)
class EssayRangeAdmin(admin.ModelAdmin):
    list_display = ('__str__',)