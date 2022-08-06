# Generated by Django 4.0.6 on 2022-08-05 18:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0008_remove_personalchatroom_group_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalchat',
            name='is_viewed',
        ),
        migrations.AddField(
            model_name='personalchat',
            name='viewed_by',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]