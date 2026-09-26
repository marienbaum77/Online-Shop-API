from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с личным балансом для покупок."""

    balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        verbose_name='Баланс',
    )

    def __str__(self):
        return self.username
