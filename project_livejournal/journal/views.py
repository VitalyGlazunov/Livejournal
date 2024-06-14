from django.shortcuts import render
from .models import Article


def home(request):
    data = Article.objects.all()
    return render(request, 'journal/home.html', {'Article': data})


def categories(request):
    return render(request, 'journal/categories.html')


def popular(request):
    return render(request, 'journal/popular.html')


def subscription(request):
    return render(request, 'journal/subscription.html')


def shop(request):
    return render(request, 'journal/shop.html')


def about_us(request):
    return render(request, 'journal/about_us.html')


def guide(request):
    return render(request, 'journal/guide.html')






