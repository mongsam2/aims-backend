from django.urls import path
from . import views

urlpatterns = [
    path("", views.StudentRecordsView.as_view()),
    path("<int:student_record_id>/", views.StudentRecordDetailView.as_view()),
    path("evaluation-categoreis/", views.StudentRecordEvaluationView.as_view()),
]
