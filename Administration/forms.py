from django import forms


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

