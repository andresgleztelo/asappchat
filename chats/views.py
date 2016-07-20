from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.template import Context, loader
from django.http import HttpResponse, JsonResponse
from chats.models import Chat, Conversation
from users.models import ChatUser
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import json
import logging

logger = logging.getLogger('chats.views')

@login_required
def home(request):
    user = request.user.chat_user
    try:
        conversations = user.conversations.filter(archived=False) \
                            .prefetch_related('participants').order_by('-updated_at')

        template = loader.get_template('chats/home.html')
        context = _get_home_page_contex(user, conversations)
        context.update(csrf(request))
    except:
        logger.exception('Error fetching conversations for chat user {}'.format(user.id))
        raise

    return HttpResponse(template.render(context))

@login_required
def get_chats(request):
    try:
        conversation = Conversation.objects.prefetch_related('chats__sender').get(
                           identifier=request.GET['conversation_id'])

        # Could use a permission class decorator instead.
        if request.user.chat_user.is_a_participant(conversation) is False:
            JsonResponse({'status': 'fail', 'reason': 'You don\'t have permission'})

        chats = []
        for chat in conversation.chats.all().order_by('created_at'):
            chats.append({'sender': chat.sender.identifier, 'content': chat.content, 'chat_id': chat.id})
    except:
        logger.exception('Error getting chats for chat user {}'.format(request.user.chat_user.id))
        raise

    return JsonResponse({'status': 'ok', 'chats': chats})

@login_required
def post_chat(request):
    sender = request.user.chat_user

    try:
        if request.POST.get('conversation_id'):
            conversation = Conversation.objects.prefetch_related('participants').get(identifier=request.POST['conversation_id'])
        else:
            conversation = Conversation.objects.create_new_conversation()

            target_participant = ChatUser.objects.get(identifier=request.POST['receiver'])
            conversation.participants.add(sender)
            conversation.participants.add(target_participant)

        # Could use a permission class decorator instead.
        if sender.is_a_participant(conversation) is False:
            JsonResponse({'status': 'fail', 'reason': 'You don\'t have permission'})

        content = request.POST['chat_content']
        chat = Chat.objects.create(sender=sender, conversation=conversation, content=content)
        send_websocket_notification_to_participants(conversation, chat, sender)
    except:
        logger.exception('Error posting chat from user {}'.format(sender.id))
        raise

    return JsonResponse({
        'status': 'ok',
        'conversation_id': conversation.identifier,
        'chat_id': chat.id})


def _get_home_page_contex(user, conversations):
    conversations_info_list = []
    for conversation in conversations:
        other_participants = conversation.get_other_participants(user)
        if len(other_participants) == 0:
            continue

        # For now, assume there is only one other paticipant in a conversation.
        conversations_info_list.append({
            'username': other_participants[0].identifier,
            'conversation_id': conversation.identifier})

    return Context({'conversations': conversations_info_list, 'current_user': user.identifier})

def send_websocket_notification_to_participants(conversation, chat, sender):
    try:
        participants = conversation.get_other_participants(sender)
        redis_publisher = RedisPublisher(facility='chat_notification', users=participants)
        message_dict = {
            'conversation_id': conversation.identifier,
            'chat_id': chat.id,
            'chat_content': chat.content,
            'sender': sender.identifier
        }
        message = RedisMessage(json.dumps(message_dict))
        redis_publisher.publish_message(message)
    except:
        logger.exception('Error sending websocket notification for conversation: {}'.format(conversation.id))
        raise
