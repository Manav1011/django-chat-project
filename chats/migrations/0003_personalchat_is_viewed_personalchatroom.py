# Generated by Django 4.0.6 on 2022-08-04 06:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0002_personalchat_delete_chats'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalchat',
            name='is_viewed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='PersonalChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('chats', models.ManyToManyField(to='chats.personalchat')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
