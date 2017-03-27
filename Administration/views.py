from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import *
from django.http import Http404

def get_auth_error(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return None
        else:
            return render(request, 'permission_denied.html')

    return render(request, 'permission_denied.html')


# Create your views here.
def index(request):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    return render(request, 'Administration/index.html')


def add_user(request):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    if request.method != 'POST':
        return render(request, 'Administration/add_user.html', {'form': AddUserForm()})
    else:
        form = AddUserForm(request.POST)
        if not form.is_valid():
            ctx = {
                'errors': ['Submitted form was not valid.'],
                'form': form,
            }
            return render(request, 'Administration/add_user.html', ctx)
        else:
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            pwd = form.cleaned_data['password']
            su = form.cleaned_data['superuser']

            if len(User.objects.filter(username=username)) != 0:
                form.add_error('username', 'Username is taken.')
                ctx = {
                    'errors': ['Submitted form was not valid.'],
                    'form': form,
                }
                return render(request, 'Administration/add_user.html', ctx)

            if su:
                user = User.objects.create_superuser(username, email=email, password=pwd)
            else:
                user = User.objects.create_user(username, email=email, password=pwd)

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            ctx = {
                'success': ['User {} was created.'.format(username)],
                'form': AddUserForm(),
            }
            return render(request, 'Administration/add_user.html', ctx)


def delete_user(request, user_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("No such user.")

    if request.method != 'POST':
        ctx = {
            'u': user
        }
        return render(request, 'Administration/delete_user.html', ctx)
    else:
        user.delete()
        return redirect('Administration:index')
