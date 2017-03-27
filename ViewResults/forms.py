from django import forms
from datetimewidget.widgets import DateTimeWidget


class FilterExperimentsForm(forms.Form):
    name_filter = forms.CharField(
        label='Search by name',
        required=False,
        max_length=255)
    sha256_filter = forms.CharField(
        label='SHA-256 of data file',
        required=False,
        max_length=64)
    date_filter_from = forms.DateTimeField(
        label='Only newer experiments than',
        required=False,
        widget=DateTimeWidget(attrs={'id': "from"}, usel10n=True, bootstrap_version=3))
    date_filter_to = forms.DateTimeField(
        label='Only older experiments than',
        required=False,
        widget=DateTimeWidget(attrs={'id': "to"}, usel10n=True, bootstrap_version=3))
    only_own = forms.BooleanField(
        label='Show only your experiments',
        required=False)