# Generated by Django 5.0.6 on 2024-06-16 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0004_alter_like_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('Рубрика №1', 'Category №1'), ('Рубрика №2', 'Category №2'), ('Рубрика №3', 'Category №3'), ('Рубрика №4', 'Category №4'), ('Рубрика №5', 'Category №5')], default='Рубрика №1', max_length=50, verbose_name='Рубрика'),
        ),
    ]
