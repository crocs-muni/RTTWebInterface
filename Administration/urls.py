from django.conf.urls import url
from . import views


app_name = 'Administration'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^AddUser/$', views.add_user, name='add_user'),
    url(r'^DeleteUser/(?P<user_id>[0-9]+)/$', views.delete_user, name='delete_user'),
]
