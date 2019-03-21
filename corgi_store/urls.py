from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('corgi/<int:corgi_id>/', views.detail, name='detail'),
    path('corgi/all/', views.browse_corgis, name='browse_corgis'),
    path('corgi/buy/', views.buy_corgi, name='buy_corgi'),
    path('list_corgi/', views.list_corgi, name='list_corgi'),
    path('sign_up/', views.sign_up, name='sign_up'),
]
