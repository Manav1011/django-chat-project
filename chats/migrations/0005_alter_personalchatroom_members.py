# Generated by Django 4.0.6 on 2022-08-04 07:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0004_alter_personalchatroom_chats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalchatroom',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
