from django.urls import path, include
from . import  views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories', views.categories, name='categories'),
    path('popular', views.popular, name='popular'),
    path('subscription', views.subscription, name='subscription'),
    path('shop', views.shop, name='shop'),
    path('about-us', views.about_us, name='about-us'),
    path('guide', views.guide, name='guide'),
]
