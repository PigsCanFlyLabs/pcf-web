from django.contrib import admin

from main.models import *

# Register your models here.
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(CartProduct)
