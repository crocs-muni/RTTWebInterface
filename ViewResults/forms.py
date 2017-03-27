from django import forms
from datetimewidget.widgets import DateTimeWidget
from urllib import parse


class FilterExperimentsForm(forms.Form):
    name = forms.CharField(
        label='Search by name',
        required=False,
        max_length=255)
    sha256 = forms.CharField(
        label='SHA-256 of data file',
        required=False,
        max_length=64)
    created_from = forms.DateTimeField(
        label='Only newer experiments than',
        required=False,
        widget=DateTimeWidget(attrs={'id': "from"}, usel10n=True, bootstrap_version=3))
    created_to = forms.DateTimeField(
        label='Only older experiments than',
        required=False,
        widget=DateTimeWidget(attrs={'id': "to"}, usel10n=True, bootstrap_version=3))
    only_own = forms.BooleanField(
        label='Show only your experiments',
        required=False)

    def as_url_args(self):
        return '?' + parse.urlencode(self.cleaned_data)
