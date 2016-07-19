from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class ChatUser(models.Model):
    """ A ChatUser corresponds to an individual user in our app. It can be associated
        with multiple conversations and chats. It has a one to one mapping to the corresponding
        auth user """
    user = models.OneToOneField(User, related_name='chat_user', on_delete=models.CASCADE)
    identifier = models.CharField(max_length=10, blank=False, null=False, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def is_a_participant(self, conversation):
        return self.conversations.filter(identifier=conversation.identifier).exists()

    def __str__(self):
        return self.identifier
