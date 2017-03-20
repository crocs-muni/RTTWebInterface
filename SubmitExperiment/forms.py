from django import forms


CONFIGS = [
    (0, 'none'),
    (1, '1MB'),
    (2, '10MB'),
    (3, '100MB'),
    (4, '1000MB'),
    (5, '8GB-default'),
]


# confDisable
class ExperimentForm(forms.Form):
    exp_name = forms.CharField(label='Experiment name',
                               max_length=255)
    in_file = forms.FileField(label='Input file')
    email = forms.EmailField(label='E-Mail for notifications',
                             max_length=255, required=False)

    default_cfg = forms.BooleanField(label='Use default configuration', required=False,
                                     widget=forms.CheckboxInput(attrs={'onclick': 'confDisable();'}))
    choose_cfg = forms.ChoiceField(choices=CONFIGS, label='Choose configuration', required=False,
                                   widget=forms.Select(attrs={'onclick': 'confDisable();'}))
    own_cfg = forms.FileField(label='Configuration file', required=False,
                              widget=forms.FileInput(attrs={'onchange': 'confDisable();'}))

    batt_sts = forms.BooleanField(label='NIST Statistical Testing Suite',
                                  required=False)
    batt_die = forms.BooleanField(label='DIEHARDER',
                                  required=False)
    batt_tu_sc = forms.BooleanField(label='TestU01 Small Crush',
                                    required=False)
    batt_tu_c = forms.BooleanField(label='TestU01 Crush',
                                   required=False)
    batt_tu_bc = forms.BooleanField(label='TestU01 Big Crush',
                                    required=False)
    batt_tu_rab = forms.BooleanField(label='TestU01 Rabbit',
                                     required=False)
    batt_tu_ab = forms.BooleanField(label='TestU01 Alphabit',
                                    required=False)
    batt_tu_bab = forms.BooleanField(label='TestU01 Block Alphabit',
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

        if not default_cfg and False and (choose_cfg is None or choose_cfg == '0') and own_cfg is None:
            raise forms.ValidationError("You must either use default configuration or choose prepared "
                                        "configuration or provide own configuration file.")

        if not sts and not die and not tu_sc and not tu_c and \
                not tu_bc and not tu_rab and not tu_ab and not tu_bab:
            raise forms.ValidationError("No batteries were set for execution.")

        return cleaned_data
