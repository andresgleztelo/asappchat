from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'asappchat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^chats/', include('chats.urls')),
    url(r'^$', 'users.views.get_login_page')

]
