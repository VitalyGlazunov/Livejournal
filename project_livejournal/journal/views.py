from django.shortcuts import get_object_or_404
from .models import Article, Comment, Like, Follow
from .forms import CommentForm
from django.contrib.auth.models import User
from users.models import Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect
from cloudipsp import Api, Checkout
import uuid
import json


class HomeView(ListView):
    model = Article
    template_name = 'journal/home.html'
    context_object_name = 'Article'
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(publication=True).order_by('-date')


class UserAllArticlesView(ListView):
    model = Article
    template_name = 'journal/user_articles.html'
    context_object_name = 'Article'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Article.objects.filter(author=user, publication=True).order_by('-date')


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'journal/articles_detail.html'

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        if not article.publication:
            raise Http404("Статья не опубликована")
        return article

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
            ctx['profile'] = profile
            ctx['comment_form'] = CommentForm()
            ctx['user_has_liked'] = Like.objects.filter(article=self.object, liked_by=user, like=True).exists()
            ctx['is_following'] = Follow.objects.filter(follower=user, following=self.object.author).exists()
        return ctx


class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'journal/create_article.html'
    fields = ['title', 'category', 'description', 'text', 'publication']

    def get_context_data(self, **kwargs):
        ctx = super(CreateArticleView, self).get_context_data(**kwargs)
        ctx['title'] = 'Добавление статьи'
        ctx['btn_text'] = 'Добавить статью'
        return ctx

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateArticleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'journal/create_article.html'
    fields = ['title', 'category', 'description', 'text', 'publication']

    def get_context_data(self, **kwargs):
        ctx = super(UpdateArticleView, self).get_context_data(**kwargs)
        ctx['title'] = 'Обновление статьи'
        ctx['btn_text'] = 'Обновить статью'
        return ctx

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        articles = self.get_object()
        if self.request.user == articles.author:
            return True
        return False


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = '/profile/'
    template_name = 'journal/articles-delete.html'

    def test_func(self):
        articles = self.get_object()
        if self.request.user == articles.author:
            return True
        return False


class CategoriesDetailView(ListView):
    model = Article
    template_name = 'journal/categories.html'
    context_object_name = 'articles'

    def get_queryset(self):
        category = self.kwargs['category']
        return Article.objects.filter(category=category, publication=True)


class PopularView(ListView):
    model = Article
    template_name = 'journal/popular.html'


class SubscriptionView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = 'journal/subscription.html'
    context_object_name = 'follows'

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def post(self, request, *args, **kwargs):
        user_to_follow = User.objects.get(pk=request.POST.get('user_id'))
        if user_to_follow != request.user:
            if Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
                Follow.objects.filter(follower=request.user, following=user_to_follow).delete()
            else:
                Follow.objects.create(follower=request.user, following=user_to_follow)
        return redirect('subscription')


class ShopView(ListView):
    model = Article
    template_name = 'journal/shop.html'

    def get_checkout_url(self, data):
        api = Api(merchant_id=1548266, secret_key='k3JSxRVX0SRUqFhLxXaGyp8LxZSM8z8D')
        checkout = Checkout(api=api)
        return checkout.url(data).get('checkout_url')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        data1 = {
            "currency": "RUB",
            "amount": 80000,
            "order_desc": "Покупка VIP статуса для пользователя на пол года",
            "order_id": str(uuid.uuid1()),
            "merchant_data": user.username
        }
        data2 = {
            "currency": "RUB",
            "amount": 150000,
            "order_desc": "Покупка VIP статуса для пользователя на год",
            "order_id": str(uuid.uuid1()),
            "merchant_data": user.username
        }
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
            ctx['profile'] = profile
            ctx['url1'] = self.get_checkout_url(data1)
            ctx['url2'] = self.get_checkout_url(data2)
        return ctx


class AboutUsView(ListView):
    model = Article
    template_name = 'journal/about_us.html'


class GuideView(ListView):
    model = Article
    template_name = 'journal/guide.html'


class AddCommentView(LoginRequiredMixin, View):

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
        return redirect('articles-detail', pk=pk)


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, View):

    def post(self, request, pk, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, article_id=pk)
        if request.user.is_superuser or comment.author == request.user:
            comment.delete()
        return redirect('articles-detail', pk=pk)

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        return self.request.user.is_superuser or self.request.user == comment.author


class AddLikeView(LoginRequiredMixin, View):

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        user = request.user

        like, created = Like.objects.get_or_create(article=article, liked_by=user)

        if not created:
            like.delete()
        else:
            like.like = True
            like.save()

        article.likes = Like.objects.filter(article=article, like=True).count()
        article.save()
        return redirect('articles-detail', pk=pk)


class CallBackPaymentView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        if username:
            user_profile = get_object_or_404(Profile, user__username=username)
            user_profile.status = 'User VIP'
            user_profile.save()


class TestShopView(LoginRequiredMixin, View):
    template_name = 'journal/shop.html'

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = {
            "username": user.username
        }
        json_string = json.dumps(data)
        data = json.loads(json_string)
        username = data.get('username')
        if request.user.is_authenticated:
            if username == user.username:
                profile = request.user.profile
                profile.status = 'User VIP'
                profile.save()
            return redirect('shop')
