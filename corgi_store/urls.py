from django.urls import include, path

from . import views
from webhook import *

urlpatterns = [
    path('', views.home, name='home'),
    path('corgi/<int:corgi_id>/', views.detail, name='detail'),
    path('corgi/all/', views.browse_corgis, name='browse_corgis'),
    path('corgi/buy/', views.buy_corgi, name='buy_corgi'),
    path('list_corgi/', views.list_corgi, name='list_corgi'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('favorite/', views.favorite_corgi, name='favorite'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_profile/close', views.close, name='close'),
    path('corgi/all/filter', views.all_filter, name='all_filter'),
    path('corgi/buy/filter', views.buy_filter, name='buy_filter'),
    path('webhook/', views.webhook)
]
