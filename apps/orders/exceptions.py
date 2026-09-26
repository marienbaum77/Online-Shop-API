class OrderError(Exception):
    """Базовое исключение для ошибок оформления заказа."""


class EmptyCartError(OrderError):
    """Корзина пуста — заказ оформить нельзя."""


class InsufficientStockError(OrderError):
    """Недостаточно товара на складе."""

    def __init__(self, product):
        self.product = product
        super().__init__(f'Недостаточно товара "{product.name}" на складе.')


class InsufficientBalanceError(OrderError):
    """Недостаточно средств на балансе пользователя."""
