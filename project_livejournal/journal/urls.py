from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('articles/add', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>', views.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<int:pk>/update', views.ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<int:pk>/delete', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('articles/<str:username>', views.UserAllArticlesView.as_view(), name='user_articles'),
    path('categories/<str:category>', views.CategoriesDetailView.as_view(), name='categories_detail'),
    path('popular', views.PopularListView.as_view(), name='popular_list'),
    path('subscription', views.SubscriptionListView.as_view(), name='subscription_list'),
    path('articles/<int:pk>/comment/add/', views.CommentCreateView.as_view(), name='add_comment'),
    path('articles/<int:pk>/comment/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('article/<int:pk>/like/', views.LikeCreateView.as_view(), name='article_add_like'),
    path('article/<int:pk>/unlike/', views.LikeDeleteView.as_view(), name='article_remove_like'),
    path('about-us', views.AboutUsListView.as_view(), name='about_us_list'),
    path('guide', views.GuideListView.as_view(), name='guide_list'),
    path('shop', views.ShopListView.as_view(), name='shop_list'),
    path('callback', views.CallBackPaymentView.as_view(), name="callback"),
    path('test-shop/', views.TestShopView.as_view(), name='test_shop'),
]
