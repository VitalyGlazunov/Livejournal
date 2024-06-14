from django.contrib import admin
from .models import Article, Comment, Follow, Like

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)


