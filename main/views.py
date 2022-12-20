from django.shortcuts import render
from django.views import View
from .models import Product
from os.path import exists
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'index.html', context={'title': 'Pigs Can Fly Labs'})


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html', context={'title': 'About Us'})


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html', context={'title': 'Contact Us'})


class ProductsView(View):
    def get(self, request):
        if "category" not in request.GET:
            return render(request, 'products.html', context={
                'title': 'Products',
                'type': 'producs',
                'products': Product.objects.all()
            })
        else:
            cat = request.GET["category"]
            cat_name = Product.Categories(cat).label
            extra_style = None
            bg_img_name = f"assets/images/{cat_name}.jpg".lower()
            if finders.find(f"{bg_img_name}"):
                extra_style = f"background-image: url('/static/{bg_img_name}');"
            return render(request, 'products.html', context={
                'title': f'Products - {cat_name}',
                'type': cat_name,
                'products': Product.objects.filter(cat=cat),
                'extra_style': extra_style
            })            


class ServicesView(View):
    def get(self, request):
        return render(request, 'services.html', context={'title': 'Services'})


class SubscribeView(View):
    def get(self, request):
        return render(request, 'subscribe_page.html', context={'title': 'Subscribe for updates'})


class ProductView(View):
    def get(self, request):
        return render(request, 'single-product.html', context={'title': 'Product Title'})

        


