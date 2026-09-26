import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger('orders')


def notify_order_created(order):
    """Логирует и (опционально) отправляет письмо об успешно созданном заказе."""

    message = (
        f'Заказ №{order.id} успешно создан пользователем {order.user.username}. '
        f'Сумма: {order.total_price}.'
    )
    logger.info(message)

    send_mail(
        subject=f'Заказ №{order.id} оформлен',
        message=message,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'shop@example.com'),
        recipient_list=[order.user.email] if order.user.email else [],
        fail_silently=True,
    )
