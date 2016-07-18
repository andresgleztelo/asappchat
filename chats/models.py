from django.db import models
from django.utils import timezone


class Conversation(models.Model):
    # The intermediary join table that represents this field will by default have an index
    # for all foreign keys.
    participants = models.ManyToManyField('users.ChatUser', related_name='conversations')

    identifier = models.CharField(max_length=10, blank=False, null=False, unique=True, db_index=True)
    archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(null=True, default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def get_other_participants(self, participant):
        return [user for user in self.participants.all() if user.identifier != participant.identifier]


class Chat(models.Model):
    CONTENT_CHOICES = (
        ('TEXT', 'A text chat.'),
        ('AUDIO', 'An audio chat.'),
        ('VIDEO', 'A video chat.')
    )

    conversation = models.ForeignKey('Conversation', null=False, related_name='chats', db_index=True)
    sender = models.ForeignKey('users.ChatUser', null=True, on_delete=models.SET_NULL, db_index=True)
    content_type = models.CharField(max_length=50, choices=CONTENT_CHOICES)
    content = models.TextField(blank=True)

    created_at = models.DateTimeField(null=True, default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)
