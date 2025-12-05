from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Report
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ReportSerializer,
)

User = get_user_model()


# --- LOGIN /auth/login ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # кастомные поля в токене
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # дополнительно вернём данные пользователя
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'role': self.user.role,
        }
        return data


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


# --- REGISTER /auth/register ---
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# --- ME /auth/me ---
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# --- REPORTS /reports ---
class ReportListCreateView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Roles.ADMIN:
            return Report.objects.all().order_by('-created_at')
        return Report.objects.filter(author=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
