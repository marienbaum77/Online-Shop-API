from django.db import transaction

from apps.cart.models import Cart

from .exceptions import EmptyCartError, InsufficientBalanceError, InsufficientStockError
from .models import Order, OrderItem
from .notifications import notify_order_created


class OrderService:
    """Бизнес-логика оформления заказа из корзины пользователя."""

    def __init__(self, user):
        self.user = user

    @transaction.atomic
    def create_order_from_cart(self):
        cart = Cart.objects.select_for_update().filter(user=self.user).first()
        items = list(cart.items.select_related('product').select_for_update()) if cart else []

        if not items:
            raise EmptyCartError('Корзина пуста.')

        # 1. Проверяем остатки на складе по каждой позиции.
        total_price = 0
        for item in items:
            if item.product.stock < item.quantity:
                raise InsufficientStockError(item.product)
            total_price += item.product.price * item.quantity

        # 2. Проверяем баланс пользователя.
        user = type(self.user).objects.select_for_update().get(pk=self.user.pk)
        if user.balance < total_price:
            raise InsufficientBalanceError('Недостаточно средств на балансе.')

        # 3. Создаём заказ и его позиции.
        order = Order.objects.create(user=user, total_price=total_price)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )
            # 4. Списываем количество со склада.
            item.product.stock -= item.quantity
            item.product.save(update_fields=['stock'])

        # 5. Списываем баланс.
        user.balance -= total_price
        user.save(update_fields=['balance'])

        # 6. Очищаем корзину.
        cart.items.all().delete()

        # 7. Уведомление/логирование об успешном заказе.
        notify_order_created(order)

        return order
