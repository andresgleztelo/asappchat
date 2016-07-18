from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template import Context, loader


def get_login_page(request):
    if request.user.is_authenticated():
        return redirect('chats.views.home')

    template = loader.get_template('users/login.html')
    context = Context()
    context.update(csrf(request))
    return HttpResponse(template.render(context))

def log_user_in(request):
    username = request.POST['username']
    user = authenticate(username=username)
    if user is not None:
        if user.chat_user.is_active:
            login(request, user)
            return redirect('chats.views.home')
        else:
            return HttpResponseBadRequest('Your account has been disabled')
    else:
        return HttpResponseBadRequest('Invalid login')

def log_user_out(request):
    logout(request)
    return redirect('users.views.get_login_page')
