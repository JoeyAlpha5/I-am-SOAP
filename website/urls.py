from django.urls import path
from .views import home, account, register, orders, stockists
from .admin import Export_Products
from django.contrib.auth  import views

urlpatterns = [
    path('', home),
    path('login', views.LoginView.as_view(template_name='website/login.html')),
    path('logout', views.LogoutView.as_view(template_name='website/login.html')),
    path('account', account),
    path('stockists', stockists),
    path('register', register),
    path('orders/<orderId>',orders),
    
]
