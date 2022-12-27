from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static
from django.urls import reverse

from main.payments import Payments
from typing import Optional


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(default="No description.")
    image = models.ImageField(upload_to='product-images')
    external_product_id = models.CharField(max_length=250, null=True, blank=True)
    product_id = models.AutoField(primary_key=True)

    def generate_external_product_id(self):
        external_product_id = Payments.create_product(
            self.name, self.description, self.price, currency="usd")
        return external_product_id

    def save(self, *args, **kwargs):
        if not self.external_product_id or True:
            self.external_product_id = self.generate_external_product_id()
        super().save(*args, **kwargs)

    class Modes(models.TextChoices):
        PAYMENT = 'P', 'payment'
        SUBSCRIPTION = 'S', 'subscription'

    class TaxTypes(models.TextChoices):
        # See https://stripe.com/docs/tax/tax-categories
        GOODS = 'txcd_99999999', 'Goods'
        SERVICES = 'txcd_20030000', 'Services'
        HOSTING = 'txcd_10701100', 'Hosting'
        PHONES = 'txcd_34021000', 'Phones'
        BOOKS = 'txcd_35010000', 'Books'  # Physical books

    class Categories(models.TextChoices):
        BOOKS = 'B', "Books"
        SERVICES = 'S', "Services"
        ELECTRONICS = 'E', "Electronics"
        MERCH = 'M', "Merch"

    name = models.CharField(max_length=250)
    page = models.CharField(
        max_length=250,
        blank=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='data_here',
        blank=True)
    image_name = models.CharField(max_length=250, default="", blank=True)
    tax_code = models.CharField(
        max_length=20,
        choices=TaxTypes.choices,
        default=TaxTypes.GOODS)
    cat = models.CharField(
        max_length=2,
        choices=Categories.choices,
        default=Categories.MERCH)
    mode = models.CharField(
        max_length=1,
        choices=Modes.choices,
        default=Modes.PAYMENT)

    def get_display_price(self) -> str:
        return "{0:.2f}".format(self.price / 100)

    def get_absolute_url(self) -> str:
        return reverse('product', kwargs={'product_id': self.product_id})

    def get_image_url(self) -> Optional[str]:
        try:
            return self.image.url
        except:
            if self.image_name is not None:
                return static(f"assets/images/{self.image_name}")
            else:
                return None

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'<Product: {self.name}>'


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        )
    products = models.ManyToManyField(
        'CartProduct', related_name='cart_products')

    def clear(self):
        self.products.remove(*self.products.all())

    def __str__(self) -> str:
        return f'{self.user.username}'

    def __repr__(self) -> str:
        return f'<Cart: {self.user.username}>'


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    price_id = models.CharField(max_length=250, null=True)

    def generate_price_id(self):
        if self.product.mode == Product.Modes.PAYMENT:
            price_id = Payments.create_price(
                self.product.external_product_id, self.product.price, currency="usd")
        else:
            price_id = Payments.create_price(
                self.product.external_product_id, self.product.price, currency="usd",
                interval="year"
            )
        return price_id
    def save(self, *args, **kwargs):
        if not self.price_id:
            self.price_id = self.generate_price_id()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.product.name}'

    def __repr__(self) -> str:
        return f'<CartProduct: {self.product.name}>'

    def total_price(self):
        return (self.product.price * self.quantity)

    def total_display_price(self):
        return "{0:.2f}".format(self.total_price() / 100)
