from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import EmptyCartError, InsufficientBalanceError, InsufficientStockError
from .models import Order
from .serializers import OrderSerializer
from .services import OrderService


class OrderListView(generics.ListAPIView):
    """Список заказов текущего пользователя."""

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


class OrderCreateView(APIView):
    """Оформление заказа из текущей корзины пользователя."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            order = OrderService(request.user).create_order_from_cart()
        except (EmptyCartError, InsufficientStockError, InsufficientBalanceError) as exc:
            raise ValidationError({'detail': str(exc)})

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    """Детали конкретного заказа текущего пользователя."""

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
