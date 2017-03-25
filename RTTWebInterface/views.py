from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from .forms import LoginForm


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated:
        # Redirect to root
        return redirect('index')

    if request.method != 'POST':
        # Show the form
        return render(request, 'login.html', {'form': LoginForm()})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
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
        else:
            ctx = {
                'errors': ['Submitted form was not valid.'],
                'form': form,
            }
            return render(request, 'login.html', ctx)
