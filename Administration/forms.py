from django import forms
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget
from SubmitExperiment.models import *
import re


class AddUserForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150)
    email = forms.EmailField(
        label='E-Mail Address')
    first_name = forms.CharField(
        label='First name',
        max_length=30,
        required=False)
    last_name = forms.CharField(
        label='Last name',
        max_length=30,
        required=False)
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput())
    password_again = forms.CharField(
        label='Password again',
        widget=forms.PasswordInput())
    superuser = forms.BooleanField(
        label='Grant superuser rights',
        required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        check_name_reg = re.compile(r'^[a-zA-Z0-9._-]+$')
        if check_name_reg.match(username) is None:
            raise forms.ValidationError("Username can contain only alphanumeric characters and - . _")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username {} is already in use.".format(username))

        return username

    def clean_password_again(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')
        if not password_again:
            raise forms.ValidationError('This field is required.')
        if password != password_again:
            raise forms.ValidationError('Passwords do not match.')

        return password_again


class EditUserForm(forms.Form):
    email = forms.EmailField(
        label='E-Mail Address')
    first_name = forms.CharField(
        label='First name',
        max_length=30,
        required=False)
    last_name = forms.CharField(
        label='Last name',
        max_length=30,
        required=False)
    password = forms.CharField(
        label='Set new password',
        required=False,
        widget=forms.PasswordInput())
    password_again = forms.CharField(
        label='Set new password again',
        required=False,
        widget=forms.PasswordInput())
    superuser = forms.BooleanField(
        label='Grant superuser rights',
        required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = user.email
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['superuser'].initial = user.is_superuser

    def clean_password_again(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')
        if password != password_again:
            raise forms.ValidationError('Passwords do not match.')

        return password_again


class AddAccessCodeForm(forms.Form):
    description = forms.CharField(
        max_length=150)
    valid_until = forms.DateTimeField(
        label='Access code will be valid until',
        widget=DateTimeWidget(
            attrs={'id': "valid_until"},
            usel10n=True,
            bootstrap_version=3))


class EditAccessCodeForm(forms.Form):
    description = forms.CharField(
        max_length=150)
    valid_until = forms.DateTimeField(
        label='Access code will be valid until',
        widget=DateTimeWidget(
            attrs={'id': "valid_until"},
            usel10n=True,
            bootstrap_version=3))
    access_code = forms.CharField(
        label='Access code',
        max_length=64)

    def __init__(self, *args, **kwargs):
        ac = kwargs.pop('access_code')
        super(EditAccessCodeForm, self).__init__(*args, **kwargs)
        self.id = ac.id
        self.fields['description'].initial = ac.description
        self.fields['valid_until'].initial = ac.valid_until
        self.fields['access_code'].initial = ac.access_code

    def clean_access_code(self):
        access_code = self.cleaned_data.get('access_code')
        check_ac_reg = re.compile(r'^[a-zA-Z0-9]+$')

        if check_ac_reg.match(access_code) is None:
            raise forms.ValidationError("Access code can contain only alphanumeric characters.")

        if AccessCode.objects.filter(access_code=access_code).exclude(id=self.id).exists():
            raise forms.ValidationError("Access code must be unique.")

        return access_code


class AddPredefinedConfiguration(forms.Form):
    name = forms.CharField(
        max_length=100)
    required_bytes = forms.IntegerField()
    description = forms.CharField(
        max_length=1000)
    cfg_file = forms.FileField(
        label="Configuration file")

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if PredefinedConfiguration.objects.filter(name=name).exists():
            raise forms.ValidationError("Name must be unique.")

        return name


class EditPredefinedConfiguration(forms.Form):
    name = forms.CharField(
        max_length=100)
    required_bytes = forms.IntegerField()
    description = forms.CharField(
        max_length=1000)
    cfg_file = forms.FileField(
        label="Configuration file")

    def __init__(self, *args, **kwargs):
        pc = kwargs.pop('pc')
        super(EditPredefinedConfiguration, self).__init__(*args, **kwargs)
        self.id = pc.id
        self.fields['name'].initial = pc.name
        self.fields['required_bytes'].initial = pc.required_bytes
        self.fields['description'].initial = pc.description
        self.fields['cfg_file'].initial = pc.cfg_file

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if PredefinedConfiguration.objects.filter(name=name).exclude(id=self.id).exists():
            raise forms.ValidationError("Name must be unique.")

        return name

