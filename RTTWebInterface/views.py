from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .forms import *


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method != 'POST':
        # Show the form
        return render(request, 'login.html', {'form': LoginForm()})
    else:
        form = LoginForm(request.POST)
        if not form.is_valid():
            ctx = {
                'errors': ['Submitted form was not valid.'],
                'form': form,
            }
            return render(request, 'login.html', ctx)

        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,
                                password=password)
            if user is not None:
                # Authentication was successful
                auth_login(request, user)
                return redirect('index')
            else:
                # Bad username/password
                ctx = {
                    'errors': ['Invalid username or password.'],
                    'form': form,
                }
                return render(request, 'login.html', ctx)


def logout(request):
    auth_logout(request)
    return redirect('index')


def password_change(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method != 'POST':
        return render(request, 'password_change.html', {'form': PasswordChangeForm()})
    else:
        form = PasswordChangeForm(request.POST)
        if not form.is_valid():
            ctx = {
                'errors': ['Submitted form was not valid.'],
                'form': form,
            }
            return render(request, 'password_change.html', ctx)
        else:
            old_pwd = form.cleaned_data['old_pwd']
            new_pwd = form.cleaned_data['new_pwd']

            if not request.user.check_password(old_pwd):
                ctx = {
                    'errors': ['Invalid current password.'],
                    'form': form,
                }
                return render(request, 'password_change.html', ctx)

            request.user.set_password(new_pwd)
            request.user.save()
            return redirect('login')
