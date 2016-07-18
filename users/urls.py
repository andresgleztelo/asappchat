from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^login/$', views.get_login_page),
    url(r'^log_user_in/$', views.log_user_in),
    url(r'^log_user_out/$', views.log_user_out)
]
