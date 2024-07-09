from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from PIL import Image


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('Analytics', 'Аналитика'),
        ('ART', 'АРТ'),
        ('Music', 'Музыка'),
        ('Science', 'Наука'),
        ('Varial', 'Разное'),
    ]
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    text = models.TextField('Основной текст')
    category = models.CharField(max_length=50, verbose_name='Рубрика', choices=CATEGORY_CHOICES, default='Разное')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    publication = models.BooleanField('Статус публикации', default=False)
    date = models.DateTimeField('Дата', default=timezone.now)
    likes = models.IntegerField('Количество лайков', default=0)
    img = models.ImageField('Превью', default='default_preview.png', upload_to='preview_images')

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.date = timezone.now()
        else:
            original = Article.objects.get(pk=self.pk)
            if self.likes == original.likes:
                self.date = timezone.now()
        super(Article, self).save(*args, **kwargs)
        image = Image.open(self.img.path)
        resize = (210, 210)
        resized_image = image.resize(resize)
        resized_image.save(self.img.path)

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
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, verbose_name='Статья')
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    like = models.BooleanField('Лайк', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.liked_by}: {self.article}{self.like}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
