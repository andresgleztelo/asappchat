from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^chats/', include('chats.urls')),
    url(r'^$', 'users.views.get_login_page')
]
