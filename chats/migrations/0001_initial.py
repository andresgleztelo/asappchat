# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type', models.CharField(max_length=50, choices=[(b'TEXT', b'A text chat.'), (b'AUDIO', b'An audio chat.'), (b'VIDEO', b'A video chat.')])),
                ('content', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(unique=True, max_length=10, db_index=True)),
                ('archived', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('participants', models.ManyToManyField(related_name='conversations', to='users.ChatUser')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='conversation',
            field=models.ForeignKey(related_name='chats', to='chats.Conversation'),
        ),
        migrations.AddField(
            model_name='chat',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='users.ChatUser', null=True),
        ),
    ]
