from django.db import models
from django.contrib.auth.models import User
from main.payments import Payments


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.FloatField(default=1.0)
    description = models.TextField(default="No description.")
    product_id = models.CharField(max_length=250, null=True)

    product_type_choices = [
        ('Space Beaver', 'Space Beaver'),
        ('Book', 'Book'),
        ('Others', 'Others'),
    ]

    type = models.CharField(max_length=12, choices=product_type_choices)

    image = models.ImageField(upload_to='product-images')

    def generate_product_id(self):
        product_id = Payments.create_product(self.name, self.description, self.price, currency="usd")
        return product_id
    
    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = self.generate_product_id()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'<Product: {self.name}>'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('CartProduct', related_name='cart_products')

    def clear(self):
        self.products.remove(*self.products.all())

    def __str__(self) -> str:
        return f'{self.user.username}'

    def __repr__(self) -> str:
        return f'<Cart: {self.user.username}>'


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.FloatField()
    price_id = models.CharField(max_length=250, null=True)

    def generate_price_id(self):
        price_id = Payments.create_price(self.product.product_id, self.product.price, currency="usd")
        return price_id

    def save(self, *args, **kwargs):
        if not self.price_id:
            self.price_id = self.generate_price_id()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.product.name}'

    def __repr__(self) -> str:
        return f'<CartProduct: {self.product.name}>'
