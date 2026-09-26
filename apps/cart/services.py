from django.core.exceptions import ValidationError

from apps.products.models import Product

from .models import Cart, CartItem


class CartService:
    """Бизнес-логика работы с корзиной пользователя, вынесенная из вьюшек."""

    def __init__(self, user):
        self.user = user

    def get_cart(self):
        cart, _ = Cart.objects.get_or_create(user=self.user)
        return cart

    def add_item(self, product_id, quantity=1):
        cart = self.get_cart()
        product = Product.objects.get(pk=product_id)
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={'quantity': quantity},
        )
        if not created:
            item.quantity += quantity
            item.save(update_fields=['quantity'])
        return item

    def update_item_quantity(self, item_id, quantity):
        if quantity < 1:
            raise ValidationError('Количество должно быть не меньше 1.')
        cart = self.get_cart()
        item = CartItem.objects.get(pk=item_id, cart=cart)
        item.quantity = quantity
        item.save(update_fields=['quantity'])
        return item

    def remove_item(self, item_id):
        cart = self.get_cart()
        CartItem.objects.filter(pk=item_id, cart=cart).delete()

    def clear(self):
        cart = self.get_cart()
        cart.items.all().delete()
