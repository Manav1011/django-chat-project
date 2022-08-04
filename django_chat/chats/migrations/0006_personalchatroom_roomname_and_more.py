# Generated by Django 4.0.6 on 2022-08-04 08:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0005_alter_personalchatroom_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalchatroom',
            name='RoomName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='personalchatroom',
            name='chats',
            field=models.ManyToManyField(to='chats.personalchat'),
        ),
        migrations.AlterField(
            model_name='personalchatroom',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
