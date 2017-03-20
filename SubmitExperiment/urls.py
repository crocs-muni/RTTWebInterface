from django.conf.urls import url
from . import views


app_name = 'SubmitExperiment'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^print_stuff/$', views.print_stuff, name='print_stuff'),
    url(r'^submit/$', views.submit, name='submit'),
]
