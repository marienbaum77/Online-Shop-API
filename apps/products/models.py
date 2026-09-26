from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    """Товар в каталоге интернет-магазина."""

    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)], verbose_name='Цена',
    )
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток на складе')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def is_in_stock(self, quantity=1):
        return self.stock >= quantity
