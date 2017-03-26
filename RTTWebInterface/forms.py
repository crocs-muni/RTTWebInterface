from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150)
    password = forms.CharField(
        widget=forms.PasswordInput())


class PasswordChangeForm(forms.Form):
    old_pwd = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput())
    new_pwd = forms.CharField(
        label="New password",
        widget=forms.PasswordInput())
    new_pwd_again = forms.CharField(
        label="New password again",
        widget=forms.PasswordInput())

    def clean_new_pwd_again(self):
        new_pwd = self.cleaned_data.get('new_pwd')
        new_pwd_again = self.cleaned_data.get('new_pwd_again')
        if not new_pwd_again:
            raise forms.ValidationError('This field is required.')
        if new_pwd != new_pwd_again:
            raise forms.ValidationError('Passwords do not match.')

        return new_pwd_again


class EditAccountForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = user.email
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
