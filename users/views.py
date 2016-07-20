from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template import Context, loader
import logging

logger = logging.getLogger('users.views')

def get_login_page(request):
    if request.user.is_authenticated():
        return redirect('chats.views.home')

    template = loader.get_template('users/login.html')
    context = Context()

    if request.session.pop('invalid_login', False):
        context['invalid_login'] = True

    context.update(csrf(request))
    return HttpResponse(template.render(context))

def log_user_in(request):
    try:
        username = request.POST['username']
        user = authenticate(username=username)
        if user is not None:
            if user.chat_user.is_active:
                login(request, user)
                return redirect('chats.views.home')
            else:
                return HttpResponseBadRequest('Your account has been disabled')
        else:
            request.session['invalid_login'] = True
            return redirect('users.views.get_login_page')
    except:
        logger.exception('Error authenticating user with username: {}'.format(request.POST.get('username')))
        raise

def log_user_out(request):
    logout(request)
    return redirect('users.views.get_login_page')
