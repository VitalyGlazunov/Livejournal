from django.shortcuts import render


def home(requst):
    return render(requst, 'journal/home.html')


def categories(requst):
    return render(requst, 'journal/categories.html')


def popular(requst):
    return render(requst, 'journal/popular.html')


def subscription(requst):
    return render(requst, 'journal/subscription.html')


def shop(requst):
    return render(requst, 'journal/shop.html')


def about_us(requst):
    return render(requst, 'journal/about_us.html')


def guide(requst):
    return render(requst, 'journal/guide.html')






