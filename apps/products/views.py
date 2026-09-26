from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Product
from .permissions import IsAdminOrReadOnly
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """CRUD для товаров. Просмотр доступен всем (включая анонимов),
    создание/изменение/удаление — только администраторам.

    `permission_classes` здесь полностью заменяет собой глобальный
    DEFAULT_PERMISSION_CLASSES (IsAuthenticated) для этого view.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['stock']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
