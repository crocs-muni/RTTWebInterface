from django.conf.urls import url
from . import views


app_name = 'SubmitExperiment'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^GainAccess/(?P<access_code>[A-Za-z0-9]+)/$', views.gain_access, name='gain_access'),
]
