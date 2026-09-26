from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.products.models import Product


class Cart(models.Model):
    """Корзина покупок пользователя (по одной на пользователя)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина пользователя {self.user}'

    @property
    def total_price(self):
        return sum((item.subtotal for item in self.items.all()), 0)


class CartItem(models.Model):
    """Позиция товара в корзине."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.product} x {self.quantity}'

    @property
    def subtotal(self):
        return self.product.price * self.quantity
