from django.urls import path
from main import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('about', views.AboutView.as_view(), name="about"),
    path('contact', views.ContactView.as_view(), name="contact"),
    path('products', views.ProductsView.as_view(), name="products"),
    path('subscribe', views.SubscribeView.as_view(), name="subscribe"),
    path('product', views.ProductView.as_view(), name="product"),
    path('services', views.ServicesView.as_view(), name="services"),
]
