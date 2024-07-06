from django.shortcuts import get_object_or_404
from .models import Article, Comment, Like, Follow
from .forms import CommentForm, ArticleForm
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
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta



class HomeView(ListView):
    model = Article
    template_name = 'journal/home.html'
    context_object_name = 'Article'
    paginate_by = 2

    def get_queryset(self):
        return Article.objects.filter(publication=True).order_by('-date')


class UserAllArticlesView(ListView):
    model = Article
    template_name = 'journal/user_articles.html'
    context_object_name = 'Article'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user == user:
            return Article.objects.filter(author=user).order_by('-date')
        return Article.objects.filter(author=user, publication=True).order_by('-date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        author = get_object_or_404(User, username=self.kwargs['username'])
        ctx['author'] = author
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
            ctx['profile'] = profile
            ctx['is_following'] = Follow.objects.filter(follower=user, following=author).exists()
        return ctx


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
    form_class = ArticleForm

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
    form_class = ArticleForm

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
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if self.request.user == articles.author:
            if not articles.publication or profile.status == 'User VIP' or self.request.user.is_superuser:
                return True
        return False

    def handle_no_permission(self):
        raise Http404("Статья не найдена или вы не имеете прав для её обновления.")


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = '/profile/'
    template_name = 'journal/articles-delete.html'
    context_object_name = 'Article'

    def test_func(self):
        articles = self.get_object()
        if self.request.user == articles.author or self.request.user.is_superuser:
            return True
        return False


class CategoriesDetailView(ListView):
    model = Article
    template_name = 'journal/categories.html'
    context_object_name = 'articles'

    def get_queryset(self):
        category = self.kwargs['category']
        return Article.objects.filter(category=category, publication=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category = self.kwargs['category']
        category_choices = dict(Article. CATEGORY_CHOICES)
        if category in category_choices:
            ctx['category'] = category_choices[category]
        return ctx


class PopularView(ListView):
    model = Article
    template_name = 'journal/popular.html'
    context_object_name = 'Article'
    peginate = 3

    def get_queryset(self):
        return Article.objects.filter(publication=True).filter(
            Q(author__profile__status='User VIP') | Q(likes__gte=5)
        ).order_by('-likes')


class SubscriptionView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = 'journal/subscription.html'
    context_object_name = 'follows'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
            ctx['profile'] = profile
        return ctx

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
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
            ctx['profile'] = profile
        return ctx

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
    template_name = 'journal/shop.html'

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
            return redirect('shop')

