from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocumentUploadView.as_view()),
    path('<int:id>/', views.DocumentUpdateView.as_view()),
    path('passfails/<int:id>/', views.PassFailPatchView.as_view())
]