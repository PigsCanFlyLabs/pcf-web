from django.urls import path
from main import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('about', views.AboutView.as_view(), name="about"),
    path('contact', views.ContactView.as_view(), name="contact"),
    path('products', views.ProductsView.as_view(), name="products"),
    path('subscribe', views.SubscribeView.as_view(), name="subscribe"),
    path('product/<int:pk>', views.ProductView.as_view(), name="product"),
    path('cart', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/<price>', views.AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:product_id>', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/success', views.CheckoutSuccessView.as_view(), name='checkout-success'),
    path('checkout/cancel', views.CheckoutCancelView.as_view(), name='checkout-cancel'),

    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]
