# Views
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Serializers
from .serializers import UserSerializer

# Django
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class RegisterView(CreateAPIView):
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # 세션 로그인 처리
            return Response({"message": "로그인 성공!"}, status=status.HTTP_200_OK)
        return Response({"error": "아이디 또는 비밀번호가 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(ensure_csrf_cookie, name="dispatch")  # CSRF 토큰을 설정하는 엔드포인트
class GetCSRFTokenView(APIView):
    def get(self, request):
        return Response({"message": "CSRF 토큰 설정됨."})

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    def post(self, request):
        logout(request)  # 세션 로그아웃 처리
        return Response({"message": "로그아웃 성공!"}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user