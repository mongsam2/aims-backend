from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentRecordsView.as_view()),
    path('<int:id>/', views.StudentRecordDetailView.as_view())
]