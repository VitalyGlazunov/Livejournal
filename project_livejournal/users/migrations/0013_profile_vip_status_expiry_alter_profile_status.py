# Generated by Django 5.0.6 on 2024-06-30 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_profile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='vip_status_expiry',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Окончание VIP статуса'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('Admin', 'Администратор'), ('User VIP', 'VIP пользователь'), ('User', 'Пользователь')], default='User', max_length=20, verbose_name='Статус пользователя'),
        ),
    ]