from django.conf.urls import url
from . import views


app_name = 'Administration'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Users
    url(r'^AddUser/$', views.add_user, name='add_user'),
    url(r'^DeleteUser/(?P<user_id>[0-9]+)/$', views.delete_user, name='delete_user'),
    url(r'^EditUser/(?P<user_id>[0-9]+)/$', views.edit_user, name='edit_user'),
    url(r'^ListUsers/$', views.list_users, name='list_users'),
    # Access Codes
    url(r'^AddAccessCode/$', views.add_access_code,
        name='add_access_code'),
    url(r'^DeleteAccessCode/(?P<access_code_id>[0-9]+)/$', views.delete_access_code,
        name='delete_access_code'),
    url(r'^EditAccessCode/(?P<access_code_id>[0-9]+)/$', views.edit_access_code,
        name='edit_access_code'),
    url(r'^ListAccessCodes/$', views.list_access_codes,
        name='list_access_codes'),
]
