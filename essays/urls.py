from django.urls import path
from . import views

urlpatterns = [
    path("", views.EssaysView.as_view()),
    path("<int:essay_id>/", views.EssayDetailView.as_view())
]
