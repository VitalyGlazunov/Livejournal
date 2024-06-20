from django.shortcuts import get_object_or_404
from .models import Article
from django.contrib.auth.models import User
from users.models import Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404


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


class CategoriesView(ListView):
    model = Article
    template_name = 'journal/categories.html'


class PopularView(ListView):
    model = Article
    template_name = 'journal/popular.html'


class SubscriptionView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'journal/subscription.html'


class ShopView(ListView):
    model = Article
    template_name = 'journal/shop.html'


class AboutUsView(ListView):
    model = Article
    template_name = 'journal/about_us.html'


class GuideView(ListView):
    model = Article
    template_name = 'journal/guide.html'