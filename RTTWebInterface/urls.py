"""RTTWebInterface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # Pages used through the RTT project
    url(r'^$', views.index, name='index'),
    url(r'^Login/$', views.login, name='login'),
    url(r'^Logout/$', views.logout, name='logout'),
    url(r'^PasswordChange/$', views.password_change, name='password_change'),
    url(r'^EditAccount/$', views.edit_account, name='edit_account'),
    url(r'^Register/$', views.register, name='register'),

    # Linking other applications
    url(r'^ViewResults/', include('ViewResults.urls')),
    url(r'^SubmitExperiment/', include('SubmitExperiment.urls')),
    url(r'^Administration/', include('Administration.urls')),
]
