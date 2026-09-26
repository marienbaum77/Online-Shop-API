from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import RegisterSerializer, TopUpBalanceSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveAPIView):
    """Профиль текущего авторизованного пользователя."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TopUpBalanceView(APIView):
    """Пополнение личного баланса текущего пользователя."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TopUpBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.balance += serializer.validated_data['amount']
        user.save(update_fields=['balance'])

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
