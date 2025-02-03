from django.urls import path
from .views import RegisterView, LoginView, GetCSRFTokenView, LogoutView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()), 
    path("csrf/", GetCSRFTokenView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', UserProfileView.as_view()),
]