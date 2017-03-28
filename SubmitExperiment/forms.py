from django import forms

from .models import PredefinedConfiguration


class ExperimentForm(forms.Form):
    # Required fields
    exp_name = forms.CharField(
        label='Experiment name',
        max_length=255)
    author_email = forms.EmailField(
        label='E-Mail',
        required=False)
    in_file = forms.FileField(
        label='Input file for batteries')

    # Configuration fields
    default_cfg = forms.BooleanField(
        label='Use default configuration (recommended)',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'onclick': 'confDisable();'}))
    choose_cfg = forms.ModelChoiceField(
        queryset=PredefinedConfiguration.objects.order_by('required_bytes'),
        label='Choose configuration',
        empty_label='----------',
        required=False,
        widget=forms.Select(attrs={'onclick': 'confDisable();'}))
    own_cfg = forms.FileField(
        label='Configuration file (advanced user)',
        required=False,
        widget=forms.FileInput(attrs={'onchange': 'confDisable();'}))

    # Battery fields
    batt_sts = forms.BooleanField(
        label='NIST Statistical Testing Suite',
        required=False)
    batt_die = forms.BooleanField(
        label='DIEHARDER',
        required=False)
    batt_tu_sc = forms.BooleanField(
        label='TestU01 Small Crush',
        required=False)
    batt_tu_c = forms.BooleanField(
        label='TestU01 Crush',
        required=False)
    batt_tu_bc = forms.BooleanField(
        label='TestU01 Big Crush (requires at least 20GB of data, 60GB for full run)',
        required=False)
    batt_tu_rab = forms.BooleanField(
        label='TestU01 Rabbit',
        required=False)
    batt_tu_ab = forms.BooleanField(
        label='TestU01 Alphabit',
        required=False)
    batt_tu_bab = forms.BooleanField(
        label='TestU01 Block Alphabit',
        required=False)

    def clean(self):
        cleaned_data = super().clean()
        default_cfg = cleaned_data.get("default_cfg")
        choose_cfg = cleaned_data.get("choose_cfg")
        own_cfg = cleaned_data.get("own_cfg")
        sts = cleaned_data.get("batt_sts")
        die = cleaned_data.get("batt_die")
        tu_sc = cleaned_data.get("batt_tu_sc")
        tu_c = cleaned_data.get("batt_tu_c")
        tu_bc = cleaned_data.get("batt_tu_bc")
        tu_rab = cleaned_data.get("batt_tu_rab")
        tu_ab = cleaned_data.get("batt_tu_ab")
        tu_bab = cleaned_data.get("batt_tu_bab")

        errors = []

        cfg_settings_sum = 0
        if default_cfg:
            cfg_settings_sum += 1
        if choose_cfg is not None:
            cfg_settings_sum += 1
        if own_cfg is not None:
            cfg_settings_sum += 1

        if cfg_settings_sum == 0:
            errors.append("You must specify configuration of the experiment.")

        if cfg_settings_sum > 1:
            errors.append("You specified multiple configurations of the experiment.")

        if not (sts or die or tu_sc or tu_c or tu_bc or tu_rab or tu_ab or tu_bab):
            errors.append("No battery was set for execution.")

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data
