"""iamsoap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth  import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('login/', include('website.urls')),
    path('logout/', include('website.urls')),
    path('register/', include('website.urls')),
    path('orders/', include('website.urls')),
    path('account/', include('website.urls')),
    path('stockists/', include('website.urls')),
    path('password-reset/',views.PasswordResetView.as_view(template_name='website/password_reset.html'), name='password_reset'),
    path('password-reset/done/',views.PasswordResetDoneView.as_view(template_name='website/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name='website/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',views.PasswordResetCompleteView.as_view(template_name='website/password_reset_complete.html'), name='password_reset_complete'),
]

handler404 = 'website.views.erroPage'

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
