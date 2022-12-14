# Generated by Django 4.0.6 on 2022-08-07 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('reciever', models.ManyToManyField(related_name='Groupreciever', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='GroupSender', to=settings.AUTH_USER_MODEL)),
                ('viewed_by', models.ManyToManyField(blank=True, null=True, related_name='GroupViewedBy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RoomName', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('chats', models.ManyToManyField(blank=True, null=True, related_name='GroupChats', to='groups.groupchat')),
                ('members', models.ManyToManyField(related_name='groupmembers', to=settings.AUTH_USER_MODEL)),
                ('members_online', models.ManyToManyField(blank=True, null=True, related_name='group_online_members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
