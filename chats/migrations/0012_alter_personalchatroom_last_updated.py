# Generated by Django 4.0.6 on 2022-08-09 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0011_alter_personalchatroom_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalchatroom',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
