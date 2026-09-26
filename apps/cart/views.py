from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product

from .models import CartItem
from .serializers import (
    AddCartItemSerializer, CartItemSerializer, CartSerializer, UpdateCartItemSerializer,
)
from .services import CartService


class CartDetailView(generics.RetrieveAPIView):
    """Просмотр текущей корзины пользователя."""

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return CartService(self.request.user).get_cart()


class CartItemListCreateView(APIView):
    """Добавление товара в корзину."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not Product.objects.filter(pk=serializer.validated_data['product_id']).exists():
            raise NotFound('Товар не найден.')

        item = CartService(request.user).add_item(
            product_id=serializer.validated_data['product_id'],
            quantity=serializer.validated_data['quantity'],
        )
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    """Изменение количества или удаление товара из корзины."""

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            item = CartService(request.user).update_item_quantity(
                item_id=item_id, quantity=serializer.validated_data['quantity'],
            )
        except CartItem.DoesNotExist:
            raise NotFound('Товар в корзине не найден.')
        except DjangoValidationError as exc:
            raise ValidationError(exc.message)

        return Response(CartItemSerializer(item).data)

    def delete(self, request, item_id):
        CartService(request.user).remove_item(item_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
