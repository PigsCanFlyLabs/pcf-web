from django.conf import settings
import stripe


class Payments:
    API_KEY = settings.STRIPE_API_KEY
    stripe.api_key = API_KEY

    @classmethod
    def create_product(cls, name: str, description: str, price: int, currency: str = "usd"):
        product = stripe.Product.create(name=name, description=description)
        product_price = stripe.Price.create(unit_amount=price, currency=currency, product=product['id'])
        print(product)
        print(product_price)

Payments.create_product("Test API", "Test APIssss", price=1200, currency="usd")

