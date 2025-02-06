from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListView.as_view()),
    path('<int:id>/<str:document_type>/', views.StudentDocumentsView.as_view()),
    path('unsuit/', views.DocumentUnsuitView.as_view())
]