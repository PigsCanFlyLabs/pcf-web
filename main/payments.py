import stripe
from django.conf import settings
from django.urls import reverse
from typing import Optional


class Payments:
    API_KEY = settings.STRIPE_API_KEY
    stripe.api_key = API_KEY

    @classmethod
    def create_product(cls, name: str, description: str, price: int, currency: str = "usd") -> str:
        product = stripe.Product.create(name=name, description=description)
        return product['id']

    @classmethod
    def create_price(cls, product_id: str, price: int, currency: str = "usd", interval: Optional[str] = None) -> str:
        product_price = None
        if interval is None:
            product_price = stripe.Price.create(
                unit_amount=price, currency=currency, product=product_id
            )
        else:
            product_price = stripe.Price.create(
                unit_amount=price, currency=currency, product=product_id,
                recurring = {"interval": interval}
            )            
        return product_price['id']

    @classmethod
    def checkout(cls, request, cart):
        products = cart.products.all()
        items = [
            {
                'price': product.price_id,
                'quantity': product.quantity,
            } for product in products
        ]

        checkout = stripe.checkout.Session.create(
            line_items=items,
            mode='subscription',
            success_url=request.build_absolute_uri(
                reverse('checkout-success')),
            cancel_url=request.build_absolute_uri(reverse('checkout-cancel')),
        )
        return checkout.url
