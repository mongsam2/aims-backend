from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocumentUploadView.as_view()),
]