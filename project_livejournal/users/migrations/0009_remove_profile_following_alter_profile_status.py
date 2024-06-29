# Generated by Django 5.0.6 on 2024-06-29 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_profile_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('User VIP', 'VIP пользователь'), ('User', 'Пользователь'), ('Admin', 'Администратор')], default='User', max_length=20, verbose_name='Статус пользователя'),
        ),
    ]
