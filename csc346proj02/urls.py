"""csc346proj02 URL Configuration

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
from django.contrib.auth import views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('corgi_store.urls')),
    # path('login/', views.login, name='login'),
    path('', include('django.contrib.auth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    # Guide for login/logout:
    # https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/
]
