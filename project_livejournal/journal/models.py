from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Модель для статьи
class Article(models.Model):
    CATEGORY_CHOICES = [
        ('Category №1', 'Рубрика №1'),
        ('Category №2', 'Рубрика №2'),
        ('Category №3', 'Рубрика №3'),
        ('Category №4', 'Рубрика №4'),
        ('Category №5', 'Рубрика №5'),
    ]
    title = models.CharField('Название', max_length=100)
    description = models.CharField('Описание', max_length=255)
    text = models.TextField('Основной текст')
    category = models.CharField(max_length=50, verbose_name='Рубрика', choices=CATEGORY_CHOICES, default='Category №1')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    publication = models.BooleanField('Статус публикации', default=False)
    date = models.DateTimeField('Дата', default=timezone.now)
    likes = models.IntegerField('Количество лайков', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name='Статья', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Комментатор', on_delete=models.CASCADE)
    text = models.TextField('Комментарий')
    date = models.DateTimeField('Дата', default=timezone.now)

    def __str__(self):
        return f'{self.article}: {self.author}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    follower = models.ForeignKey(User, verbose_name='Подписчик', on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, verbose_name='Кумир',  on_delete=models.CASCADE, related_name='followers')
    date = models.DateTimeField('Дата', default=timezone.now)

    def __str__(self):
        return f'{self.following}: {self.follower}'

    class Meta:
        verbose_name = 'Подписку'
        verbose_name_plural = 'Подписки'


class Like(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name='Cтатья', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)