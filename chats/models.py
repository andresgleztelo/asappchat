from django.db import models
from django.utils import timezone
from asappchat.utils import generate_random_str
import string


class ConversationManager(models.Manager):
    def create_new_conversation(self):
        new_conversation_identifier = generate_random_str(length=10, allowed_chars=string.ascii_uppercase + string.digits)
        while Conversation.objects.filter(identifier=new_conversation_identifier).exists():
            new_conversation_identifier = generate_random_str(length=10, allowed_chars=string.ascii_uppercase + string.digits)

        return self.create(identifier=new_conversation_identifier)


class Conversation(models.Model):
    """ A conversation is composed of participants and chats. It can be either archived
        or active. """
    # The intermediary join table that represents this field will by default have an index
    # for all foreign keys.
    participants = models.ManyToManyField('users.ChatUser', related_name='conversations')

    identifier = models.CharField(max_length=10, blank=False, null=False, unique=True, db_index=True)
    archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(null=True, default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    objects = ConversationManager()

    def get_other_participants(self, participant):
        return [user for user in self.participants.all() if user.identifier != participant.identifier]


class Chat(models.Model):
    """ A chat belongs to a conversation and a sender user. The content of the chat can be
        of type text, audio, or video """
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
