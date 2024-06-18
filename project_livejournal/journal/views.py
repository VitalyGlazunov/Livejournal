from django.shortcuts import render
from .models import Article
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class HomeView(ListView):
    model = Article
    template_name = 'journal/home.html'
    context_object_name = 'Article'
    ordering = ['-date']
    paginate_by = 3


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'journal/articles_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
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


def categories(request):
    return render(request, 'journal/categories.html')


def popular(request):
    return render(request, 'journal/popular.html')


@login_required
def subscription(request):
    return render(request, 'journal/subscription.html')


def shop(request):
    return render(request, 'journal/shop.html')


def about_us(request):
    return render(request, 'journal/about_us.html')


def guide(request):
    return render(request, 'journal/guide.html')






