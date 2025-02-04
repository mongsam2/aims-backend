from django.urls import path
from .views import ApplicantTypesView

urlpatterns = [
    path('applicant-types/', ApplicantTypesView.as_view()),
]