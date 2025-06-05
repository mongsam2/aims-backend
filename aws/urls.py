from django.urls import path
from . import views


urlpatterns = [path("presigned-url/", views.S3PresignedUrlView.as_view())]
