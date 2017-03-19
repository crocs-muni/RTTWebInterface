from django.conf.urls import url
from . import views


app_name = 'ViewResults'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Experiment/(?P<experiment_id>[0-9]+)/$', views.experiment, name='experiment'),
    url(r'^Battery/(?P<battery_id>[0-9]+)/$', views.battery, name='battery'),
    url(r'^Test/(?P<test_id>[0-9]+)/$', views.test, name='test'),
    url(r'^Variant/(?P<variant_id>[0-9]+)/$', views.variant, name='variant'),
    url(r'^Subtest/(?P<subtest_id>[0-9]+)/$', views.subtest, name='subtest')
]
