from django.urls import path, include
from . import  views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('articles/<int:pk>', views.ArticleDetailView.as_view(), name='articles-detail'),
    path('articles/add', views.CreateArticleView.as_view(), name='articles-add'),
    path('articles/<int:pk>/update', views.UpdateArticleView.as_view(), name='articles-update'),
    path('articles/<int:pk>/delete', views.DeleteArticleView.as_view(), name='articles-delete'),
    path('categories', views.categories, name='categories'),
    path('popular', views.popular, name='popular'),
    path('subscription', views.subscription, name='subscription'),
    path('shop', views.shop, name='shop'),
    path('about-us', views.about_us, name='about-us'),
    path('guide', views.guide, name='guide'),
]
