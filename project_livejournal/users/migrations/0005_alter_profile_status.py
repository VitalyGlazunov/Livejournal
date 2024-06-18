# Generated by Django 5.0.6 on 2024-06-18 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('User VIP', 'VIP пользователь'), ('User', 'Пользователь'), ('Admin', 'Администратор')], default='User', max_length=20, verbose_name='Статус пользователя'),
        ),
    ]
