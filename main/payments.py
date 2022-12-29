import stripe
from django.conf import settings
from django.urls import reverse
from typing import Optional


class Payments:
    # mypy can't find this but it does exist. idk.
    API_KEY = settings.STRIPE_API_KEY # type: ignore
    stripe.api_key = API_KEY

    @classmethod
    def create_product(cls, name: str, description: str, price: int, currency: str = "usd") -> str:
        product = stripe.Product.create(
            name=name, description=description)
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
        from main.models import Product
        products = cart.products.all()
        items = [
            {
                'price': product.price_id,
                'quantity': product.quantity,
                "adjustable_quantity": {"enabled": True},
            } for product in products
        ]
        # Add shipping if only physical products. Stripe checkout does not support
        # shipping with subscriptions so for now free shipping with any subscription
        shipping = {}
        mode = "subscription"
        product_modes = list(map(lambda x: x.product.mode, products))
        if all(map (lambda x: x == Product.Modes.PAYMENT, product_modes)):
            mode="payment"
            # options
            shipping_options = map(lambda x: {"shipping_rate": x},
                                   [
                                       "shr_0MJrIYnkDnSOC1s7fthNSlhb", # sf only
                                       "shr_0MJrL4nkDnSOC1s7cPSy15CO", #media mail
                                       "shr_0MJrMVnkDnSOC1s7xsYs0Nsa", #priority express
                                       "shr_0MJrPInkDnSOC1s7tidX8eMN", # YOLO
                                   ])
            shipping["shipping_options"] = list(shipping_options)

        if any(map (lambda x: x == Product.Modes.PAYMENT, product_modes)):
            shipping["shipping_address_collection"] = {"allowed_countries": ["US", "CA"]}

        checkout = stripe.checkout.Session.create(
            line_items=items,
            mode=mode,
            success_url=request.build_absolute_uri(
                reverse('checkout-success')),
            cancel_url=request.build_absolute_uri(reverse('checkout-cancel')),
            ** shipping,
        )
        return checkout.url
