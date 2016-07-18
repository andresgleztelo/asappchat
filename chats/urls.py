from django.conf.urls import url
from chats import views

urlpatterns = [
    url(r'^home/$', views.home),
    url(r'^get_chats/$', views.get_chats),
    url(r'^post_chat/$', views.post_chat)
]
