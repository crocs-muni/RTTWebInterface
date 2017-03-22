from django.conf.urls import url
from . import views


app_name = 'SubmitExperiment'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<access_code>[A-Za-z0-9]+)/$', views.index, name='index'),
]
