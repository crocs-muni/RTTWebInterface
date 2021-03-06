from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from .forms import *
from django.http import Http404
from SubmitExperiment.models import *
import string
import sys
import random


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


####################
# Users management #
####################
def add_user(request):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    if request.method != 'POST':
        return render(request, 'Administration/add_user.html', {'form': AddUserForm()})

    form = AddUserForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Submitted form was not valid.')
        return render(request, 'Administration/add_user.html', {'form': form})

    username = form.cleaned_data['username']
    email = form.cleaned_data['email']
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    pwd = form.cleaned_data['password']
    su = form.cleaned_data['superuser']

    if su:
        user = User.objects.create_superuser(username, email=email, password=pwd)
    else:
        user = User.objects.create_user(username, email=email, password=pwd)

    user.first_name = first_name
    user.last_name = last_name
    user.save()

    messages.success(request, 'User {} was created.'.format(username))
    return redirect('Administration:list_users')


def delete_user(request, u_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    try:
        user = User.objects.get(id=u_id)
    except User.DoesNotExist:
        raise Http404("No such user.")

    if request.method != 'POST':
        return render(request, 'Administration/delete_user.html', {'u': user})

    username = user.username
    user.delete()
    messages.success(request, 'User {} was deleted.'.format(username))
    return redirect('Administration:list_users')


def edit_user(request, u_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    try:
        user = User.objects.get(id=u_id)
    except User.DoesNotExist:
        raise Http404("No such user.")

    if request.method != 'POST':
        ctx = {
            'u': user,
            'form': EditUserForm(user=user),
        }
        return render(request, 'Administration/edit_user.html', ctx)

    form = EditUserForm(request.POST, user=user)
    if not form.is_valid():
        ctx = {
            'u': user,
            'form': form,
        }
        messages.error(request, 'Submitted form was not valid.')
        return render(request, 'Administration/edit_user.html', ctx)

    # Password validation in here not in form. In form
    # I don't know whether the pwd was changed or not.
    pwd = form.cleaned_data['password']
    if pwd is not None and len(pwd) > 0:
        try:
            validate_password(pwd)
        except forms.ValidationError as errors:
            for e in errors.messages:
                form.add_error('password', "{}".format(e))
            ctx = {
                'u': user,
                'form': form,
            }
            messages.error(request, 'Submitted form was not valid.')
            return render(request, 'Administration/edit_user.html', ctx)

        user.set_password(pwd)

    user.email = form.cleaned_data['email']
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    user.is_superuser = form.cleaned_data['superuser']
    user.save()
    messages.success(request, 'User {} was modified.'.format(user.username))
    return redirect('Administration:list_users')


def list_users(request):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    ctx = {
        'users': User.objects.all()
    }
    return render(request, 'Administration/list_users.html', ctx)


###########################
# Access codes management #
###########################
def get_rnd_code(password_len=64):
    characters = string.ascii_letters + string.digits
    return "".join(random.SystemRandom().choice(characters)
                   for _ in range(password_len))


def add_access_code(request):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    if request.method != 'POST':
        return render(request, 'Administration/add_access_code.html',
                      {'form': AddAccessCodeForm()})

    form = AddAccessCodeForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Submitted form was not valid.')
        return render(request, 'Administration/add_access_code.html', {'form': form})

    description = form.cleaned_data['description']
    valid_until = form.cleaned_data['valid_until']
    while True:
        code = get_rnd_code(64)
        # Well this is not very probable to happen...
        # More specifically, the probability is 1/(62^64)
        if not AccessCode.objects.filter(access_code=code).exists():
            break
    ac = AccessCode(description=description,
                    valid_until=valid_until,
                    access_code=code)
    ac.save()
    messages.success(request, 'Access code {} was created.'.format(ac.id))
    return redirect('Administration:list_access_codes')


def delete_access_code(request, a_c_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    try:
        ac = AccessCode.objects.get(id=a_c_id)
    except AccessCode.DoesNotExist:
        raise Http404("No such access code.")

    ac.delete()
    messages.success(request, 'Access code {} was deleted.'.format(a_c_id))
    return redirect('Administration:list_access_codes')


def edit_access_code(request, a_c_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    try:
        ac = AccessCode.objects.get(id=a_c_id)
    except AccessCode.DoesNotExist:
        raise Http404("No such access code.")

    if request.method != 'POST':
        ctx = {
            'ac': ac,
            'form': EditAccessCodeForm(access_code=ac),
        }
        return render(request, 'Administration/edit_access_code.html', ctx)

    form = EditAccessCodeForm(request.POST, access_code=ac)
    if not form.is_valid():
        messages.error(request, 'Submitted form was not valid.')
        ctx = {
            'ac': ac,
            'form': form,
        }
        return render(request, 'Administration/edit_access_code.html', ctx)

    ac.description = form.cleaned_data['description']
    ac.valid_until = form.cleaned_data['valid_until']
    ac.access_code = form.cleaned_data['access_code']
    ac.save()
    messages.success(request, 'Access code {} was modified.'.format(ac.id))
    return redirect('Administration:list_access_codes')


def list_access_codes(request):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    ctx = {
        'access_codes': AccessCode.objects.all().order_by('-valid_until'),
    }
    return render(request, 'Administration/list_access_codes.html', ctx)


def add_predefined_configuration(request):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    if request.method != 'POST':
        return render(request, 'Administration/add_predefined_configuration.html',
                      {'form': AddPredefinedConfiguration()})

    form = AddPredefinedConfiguration(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, 'Submitted form was not valid.')
        return render(request, 'Administration/add_predefined_configuration.html',
                      {'form': form})

    pc = PredefinedConfiguration(
        name=form.cleaned_data['name'],
        required_bytes=form.cleaned_data['required_bytes'],
        description=form.cleaned_data['description'],
        cfg_file=request.FILES['cfg_file'])
    pc.save()
    messages.success(request, 'Configuration {} was created.'.format(pc.name))
    return redirect('Administration:list_predefined_configurations')


def delete_predefined_configuration(request, p_c_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    try:
        pc = PredefinedConfiguration.objects.get(id=p_c_id)
    except PredefinedConfiguration.DoesNotExist:
        raise Http404("No such predefined configuration.")

    name = pc.name
    pc.delete()
    messages.success(request, 'Configuration {} was deleted.'.format(name))
    return redirect('Administration:list_predefined_configurations')


def edit_predefined_configuration(request, p_c_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    try:
        pc = PredefinedConfiguration.objects.get(id=p_c_id)
    except PredefinedConfiguration.DoesNotExist:
        raise Http404("No such predefined configuration.")

    if request.method != 'POST':
        ctx = {
            'pc': pc,
            'form': EditPredefinedConfiguration(pc=pc),
        }
        return render(request, 'Administration/edit_predefined_configuration.html', ctx)

    form = EditPredefinedConfiguration(request.POST, request.FILES, pc=pc)
    if not form.is_valid():
        ctx = {
            'pc': pc,
            'form': form
        }
        messages.error(request, 'Submitted form was not valid.')
        return render(request, 'Administration/edit_predefined_configuration.html', ctx)

    pc.name = form.cleaned_data['name']
    pc.required_bytes = form.cleaned_data['required_bytes']
    pc.description = form.cleaned_data['description']
    if request.FILES.get('cfg_file', None) is not None:
        pc.cfg_file = request.FILES['cfg_file']

    pc.save()
    messages.success(request, 'Configuration {} ({}) was modified.'
                     .format(pc.name, pc.id))
    return redirect('Administration:list_predefined_configurations')


def list_predefined_configurations(request):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    ctx = {
        'configurations': PredefinedConfiguration.objects.all().order_by('required_bytes'),
    }
    return render(request, 'Administration/list_predefined_configurations.html', ctx)
