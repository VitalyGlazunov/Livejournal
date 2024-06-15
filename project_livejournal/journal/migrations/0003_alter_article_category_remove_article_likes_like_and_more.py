# Generated by Django 5.0.6 on 2024-06-14 20:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_alter_article_options_article_category_article_likes_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('Category №1', 'Рубрика №1'), ('Category №2', 'Рубрика №2'), ('Category №3', 'Рубрика №3'), ('Category №4', 'Рубрика №4'), ('Category №5', 'Рубрика №5')], default='Category №1', max_length=50, verbose_name='Рубрика'),
        ),
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.article', verbose_name='Cтатья')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='Количество лайков'),
        ),
    ]