from django.contrib.auth.models import User

class UserAuthBackend(object):
    def authenticate(self, username=None):
        try:
            return User.objects.select_related('chat_user').get(username=username)
        except User.DoesNotExist:
            pass

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
