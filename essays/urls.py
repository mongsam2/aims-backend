from django.urls import path
from . import views

urlpatterns = [
    path('', views.EssaysView.as_view()),
    path('<int:id>/', views.EssayDetailView.as_view()),
]