from django.db import models
from django.urls import reverse



# Create your models here.
class Product(models.Model):

    class Modes(models.TextChoices):
        PAYMENT = 'P', 'payment'
        SUBSCRIPTION = 'S', 'subscription'

    class TaxTypes(models.TextChoices):
        # See https://stripe.com/docs/tax/tax-categories
        GOODS = 'G', 'txcd_99999999'
        SERVICES = 'S', 'txcd_20030000'
        HOSTING = 'H', 'txcd_10701100'
        PHONES = 'P', 'txcd_34021000'
        BOOKS = 'B', 'txcd_35010000' # Physical books

    class Categories(models.TextChoices):
        BOOKS = 'B', "Books"
        SERVICES = 'S', "Services"
        ELECTRONICS = 'E', "Electronics"
        MISC = 'M', "Merch"
    
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    page = models.CharField(
        max_length=250,
        blank=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product-images')
    image_name = models.CharField(max_length=250)
    tax_code = models.CharField(
        max_length=2,
        choices=TaxTypes.choices,
        default=TaxTypes.GOODS)
    cat = models.CharField(
        max_length=2,
        choices=Categories.choices,
        default=Categories.MISC)
    mode = models.CharField(
        max_length=1,
        choices=Modes.choices,
        default=Modes.PAYMENT)
    

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'<Product: {self.name}>'

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

    def get_absolute_url(self):
        return reverse(['product', (self.product_id,)])

    def get_image_url(self):
        if self.image is not None:
            return reverse(['static', f"assets/product-images/{self.image}"])
        else:
            return reverse(['static', f"assets/images/{self.image_name}"])
