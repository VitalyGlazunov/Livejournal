# Generated by Django 5.0.6 on 2024-06-29 15:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0007_alter_article_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name': 'Лайк статьи', 'verbose_name_plural': 'Лайки статей'},
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.AddField(
            model_name='like',
            name='like',
            field=models.BooleanField(default=False, verbose_name='Like'),
        ),
        migrations.AddField(
            model_name='like',
            name='liked_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Поставил лайк'),
        ),
        migrations.AlterField(
            model_name='like',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='journal.article', verbose_name='Публикация в статье'),
        ),
    ]
