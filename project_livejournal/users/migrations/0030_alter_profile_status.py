# Generated by Django 5.0.6 on 2024-07-08 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_alter_profile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('Admin', 'Администратор'), ('User', 'Пользователь'), ('User VIP', 'VIP пользователь')], default='User', max_length=20, verbose_name='Статус пользователя'),
        ),
    ]
