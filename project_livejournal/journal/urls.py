from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('articles/<int:pk>', views.ArticleDetailView.as_view(), name='articles-detail'),
    path('articles/add', views.CreateArticleView.as_view(), name='articles-add'),
    path('articles/<int:pk>/update', views.UpdateArticleView.as_view(), name='articles-update'),
    path('articles/<int:pk>/delete', views.DeleteArticleView.as_view(), name='articles-delete'),
    path('articles/<str:username>', views.UserAllArticlesView.as_view(), name='user-articles'),
    path('categories/<str:category>', views.CategoriesDetailView.as_view(), name='categories'),
    path('popular', views.PopularView.as_view(), name='popular'),
    path('subscription', views.SubscriptionView.as_view(), name='subscription'),
    path('shop', views.ShopView.as_view(), name='shop'),
    path('about-us', views.AboutUsView.as_view(), name='about-us'),
    path('guide', views.GuideView.as_view(), name='guide'),
]
