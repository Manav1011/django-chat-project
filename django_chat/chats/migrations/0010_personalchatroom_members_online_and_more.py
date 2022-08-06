# Generated by Django 4.0.6 on 2022-08-05 18:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0009_remove_personalchat_is_viewed_personalchat_viewed_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalchatroom',
            name='members_online',
            field=models.ManyToManyField(blank=True, null=True, related_name='online_members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='personalchatroom',
            name='members',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]