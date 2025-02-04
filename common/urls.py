from django.urls import path
from .views import ApplicantTypesView, DocumentTypesView

urlpatterns = [
    path('applicant-types/', ApplicantTypesView.as_view()),
    path('document-types/', DocumentTypesView.as_view()),
]