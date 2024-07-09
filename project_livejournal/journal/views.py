from datetime import timedelta
import math
import uuid
import json

from cloudipsp import Api, Checkout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import ArticleForm, CommentForm
from .models import Article, Comment, Follow, Like
from users.models import Profile


key = 'k3JSxRVX0SRUqFhLxXaGyp8LxZSM8z8D'
merchant_id = 1548266


class IndexView(ListView):
    model = Article
    template_name = 'journal/index.html'
    context_object_name = 'articles'
    paginate_by = 2

    def get_queryset(self):
        return Article.objects.filter(publication=True).order_by('-date')


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'journal/article_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(ArticleCreateView, self).get_context_data(**kwargs)
        ctx['btn_text'] = 'Создать статью'
        ctx['title'] = 'Создание статьи'
        return ctx

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.pk})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'journal/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        article = self.get_object()
        if not article.publication and (user != article.author):
            raise Http404("Страница не найдена. Ошибка 404.")
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
            ctx['profile'] = profile
            ctx['comment_form'] = CommentForm()
            ctx['is_following'] = (Follow.objects.filter(follower=user, following=self.object.author).exists())
            ctx['user_has_liked'] = (Like.objects.filter(article=self.object, liked_by=user, like=True).exists())
        return ctx


class UserAllArticlesView(ListView):
    model = Article
    template_name = 'journal/user_articles.html'
    context_object_name = 'articles'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        author = get_object_or_404(User, username=self.kwargs['username'])
        ctx['author'] = author
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
            ctx['profile'] = profile
            ctx['is_following'] = Follow.objects.filter(follower=user, following=author).exists()
        if user != author:
            ctx['title'] = 'Статьи пользователя'
            ctx['title_user'] = author
        else:
            ctx['title'] = 'Мои статьи'
        return ctx

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user == author:
            return Article.objects.filter(author=author).order_by('-date')
        return Article.objects.filter(author=author, publication=True).order_by('-date')


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'journal/article_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(ArticleUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = 'Обновление статьи'
        ctx['btn_text'] = 'Обновить статью'
        return ctx

    def test_func(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        article = self.get_object()
        if self.request.user == article.author:
            if (
                not article.publication or
                profile.status == 'User VIP' or
                self.request.user.is_superuser
            ):
                return True
        raise Http404("Статья не найдена или у вас нет прав для её обновления.")


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'journal/article_delete.html'
    context_object_name = 'article'

    def get_success_url(self):
        return reverse_lazy('user_articles', kwargs={'username': self.object.author.username})

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author or self.request.user.is_superuser:
            return True
        raise Http404("Статья не найдена или у вас нет прав для её удаления.")


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'article_detail.html'

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.article = article
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.kwargs['pk']})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'article_detail.html'

    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_id')
        queryset = self.get_queryset()
        obj = queryset.get(pk=comment_id)
        return obj

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.article.pk})

    def test_func(self):
        comment = self.get_object()
        if self.request.user.is_superuser or self.request.user == comment.author:
            return True
        raise Http404("Вы не можете удалить комментарий.")


class LikeCreateView(LoginRequiredMixin, CreateView):
    model = Like
    template_name = 'article_detail.html'
    fields = []

    def form_valid(self, form):
        user = self.request.user
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        like, created = Like.objects.get_or_create(article=article, liked_by=user)
        if created:
            like.like = True
            like.save()
        article.likes = Like.objects.filter(article=article, like=True).count()
        article.save()
        return redirect('article_detail', pk=self.kwargs['pk'])


class LikeDeleteView(LoginRequiredMixin, DeleteView):
    model = Like
    template_name = 'article_detail.html'

    def get_object(self, queryset=None):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        return get_object_or_404(Like, article=article, liked_by=self.request.user)

    def post(self, request, *args, **kwargs):
        like = self.get_object()
        like.delete()
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        article.likes = Like.objects.filter(article=article, like=True).count()
        article.save()
        return redirect('article_detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.kwargs['pk']})


class SubscriptionListView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = 'journal/subscription_list.html'
    context_object_name = 'heros'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            heros_users = Follow.objects.filter(follower=user)
            heros_id = heros_users.values_list('following_id', flat=True)
            ctx['heros_id'] = heros_id
        return ctx

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user).order_by('-date')

    @staticmethod
    def post(request, *args, **kwargs):
        user_to_follow = User.objects.get(pk=request.POST.get('user_id'))
        if user_to_follow != request.user:
            if Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
                Follow.objects.filter(follower=request.user, following=user_to_follow).delete()
            else:
                Follow.objects.create(follower=request.user, following=user_to_follow)
        return redirect('subscription_list')


class CategoriesDetailView(ListView):
    model = Article
    template_name = 'journal/categories_detail.html'
    context_object_name = 'articles'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category = self.kwargs['category']
        category_choices = dict(Article. CATEGORY_CHOICES)
        if category in category_choices:
            ctx['category_ru'] = category_choices[category]
            ctx['categorys_en'] = category
        return ctx

    def get_queryset(self):
        category = self.kwargs['category']
        return Article.objects.filter(category=category, publication=True).order_by('-date')


class PopularListView(ListView):
    model = Article
    template_name = 'journal/popular_list.html'
    context_object_name = 'articles'
    paginate_by = 2

    def get_queryset(self):
        users_count = User.objects.filter().distinct().count()
        popularity_threshold = math.floor(users_count * 0.1)
        if popularity_threshold == 0:
            popularity_threshold = 1
        return Article.objects.filter(publication=True).filter(
            Q(author__profile__status='User VIP') | Q(likes__gte=popularity_threshold)
        ).order_by('-likes')


class AboutUsListView(ListView):
    model = Article
    template_name = 'journal/about_us_list.html'


class GuideListView(ListView):
    model = Article
    template_name = 'journal/guide_list.html'


class ShopListView(ListView):
    model = Article
    template_name = 'journal/shop_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
            ctx['profile'] = profile
        return ctx

    def get_checkout_url(self, data):
        api = Api(merchant_id=merchant_id, secret_key=key)
        checkout = Checkout(api=api)
        return checkout.url(data).get('checkout_url')

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        user = self.request.user
        if action == 'upgrade_to_vip_half_year' and user.is_authenticated:
            data2 = {
                "currency": "RUB",
                "amount": 80000,
                "order_desc": "Покупка VIP статуса для пользователя на пол года",
                "order_id": str(uuid.uuid1()),
                "merchant_data": request.user.username
            }
            return redirect(self.get_checkout_url(data2))
        elif action == 'upgrade_to_vip_year' and user.is_authenticated:
            data1 = {
                "currency": "RUB",
                "amount": 150000,
                "order_desc": "Покупка VIP статуса для пользователя на год",
                "order_id": str(uuid.uuid1()),
                "merchant_data": request.user.username
            }
            return redirect(self.get_checkout_url(data1))
        return redirect('user')


class CallBackPaymentView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('merchant_data')
        amount = data.get('amount')
        catalog = {
            15000: 31,
            80000: 183,
            150000: 365
        }
        if username and amount in data:
            vip_status_expiry_days = catalog[amount]
            user_profile = get_object_or_404(Profile, user__username=username)
            user_profile.status = 'User VIP'
            user_profile.vip_status_expiry = timezone.now() + timedelta(days=vip_status_expiry_days)
            user_profile.save()


class TestShopView(LoginRequiredMixin, View):
    template_name = 'journal/shop_list.html'

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = {
            "merchant_data": user.username,
        }
        json_string = json.dumps(data)
        data = json.loads(json_string)
        username = data.get('merchant_data')
        if request.user.is_authenticated:
            if username == user.username:
                profile = request.user.profile
                profile.status = 'User VIP'
                profile.vip_status_expiry = timezone.now() + timedelta(seconds=10)
                profile.save()
            return redirect('shop_list')
