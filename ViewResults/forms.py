from django import forms


class FilterExperimentsForm(forms.Form):
    only_own = forms.BooleanField(label='Show only your experiments', required=False)
    name_filter = forms.CharField(label='Search by name', required=False, max_length=255)
    date_filter_from = forms.DateTimeField(label='Only newer experiments', required=False)
    date_filter_to = forms.DateTimeField(label='Only older experiments', required=False)
