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
