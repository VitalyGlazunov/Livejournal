from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    STATUS_CHOICES = {
        ('User', 'Пользователь'),
        ('User VIP', 'VIP пользователь'),
        ('Admin', 'Администратор'),
    }
    user = models.OneToOneField(User, verbose_name='Имя пользователя', on_delete=models.CASCADE)
    img = models.ImageField('Фото пользователя', default='default_user.png', upload_to='user_images')
    status = models.CharField(max_length=20, verbose_name='Статус пользователя', choices=STATUS_CHOICES, default='User')
    vip_status_expiry = models.DateTimeField(verbose_name='Окончание VIP статуса', null=True, blank=True)
    def __str__(self):
        return f'Профайл пользователя {self.user.username}'

    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.img.path)
        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)
    class Meta:
        verbose_name = 'Профаил'
        verbose_name_plural = 'Профайлы'


