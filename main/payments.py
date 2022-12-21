from django.conf import settings
from django.urls import reverse
import stripe


class Payments:
    API_KEY = settings.STRIPE_API_KEY
    stripe.api_key = API_KEY

    @classmethod
    def create_product(cls, name: str, description: str, price: int, currency: str = "usd") -> str:
        product = stripe.Product.create(name=name, description=description)
        return product['id']

    @classmethod
    def create_price(cls, product_id: str, price: float, currency: str = "usd") -> str:
        price = int(price * 100) # Convert to cents
        product_price = stripe.Price.create(unit_amount=price, currency=currency, product=product_id)
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
            mode='payment',
            success_url=request.build_absolute_uri(reverse('checkout-success')),
            cancel_url=request.build_absolute_uri(reverse('checkout-cancel')),
        )
        return checkout.url
