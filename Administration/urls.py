from django.conf.urls import url
from . import views


app_name = 'Administration'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Users
    url(r'^AddUser/$', views.add_user, name='add_user'),
    url(r'^DeleteUser/(?P<u_id>[0-9]+)/$', views.delete_user, name='delete_user'),
    url(r'^EditUser/(?P<u_id>[0-9]+)/$', views.edit_user, name='edit_user'),
    url(r'^ListUsers/$', views.list_users, name='list_users'),

    # Access Codes
    url(r'^AddAccessCode/$', views.add_access_code,
        name='add_access_code'),
    url(r'^DeleteAccessCode/(?P<a_c_id>[0-9]+)/$', views.delete_access_code,
        name='delete_access_code'),
    url(r'^EditAccessCode/(?P<c_c_id>[0-9]+)/$', views.edit_access_code,
        name='edit_access_code'),
    url(r'^ListAccessCodes/$', views.list_access_codes,
        name='list_access_codes'),

    # Predefined configurations
    url(r'^AddPredefinedConfiguration/$',
        views.add_predefined_configuration,
        name='add_predefined_configuration'),
    url(r'^DeletePredefinedConfiguration/(?P<p_c_id>[0-9]+)/$',
        views.delete_predefined_configuration,
        name='delete_predefined_configuration'),
    url(r'^EditPredefinedConfiguration/(?P<p_c_id>[0-9]+)/$',
        views.edit_predefined_configuration,
        name='edit_predefined_configuration'),
    url(r'^ListPredefinedConfigurations/$',
        views.list_predefined_configurations,
        name='list_predefined_configurations'),
]
