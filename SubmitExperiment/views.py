from django.shortcuts import render
from .forms import ExperimentForm
from django.core.files.storage import FileSystemStorage
from .models import PredefinedConfiguration
import subprocess
import shlex
import os
import _thread


# Path to submit_experiment executable relative
# to root directory of Django project
SUBMIT_EXPERIMENT_BINARY = 'SubmitExperiment/submit_binary/submit_experiment'


def submit_experiment(form, in_file_path, cfg_file_path):
    args_str = os.path.abspath(SUBMIT_EXPERIMENT_BINARY)
    if form.cleaned_data['batt_sts']:
        args_str += ' --nist_sts '
    if form.cleaned_data['batt_die']:
        args_str += ' --dieharder '
    if form.cleaned_data['batt_tu_sc']:
        args_str += ' --tu01_smallcrush '
    if form.cleaned_data['batt_tu_c']:
        args_str += ' --tu01_crush '
    if form.cleaned_data['batt_tu_bc']:
        args_str += ' --tu01_bigcrush '
    if form.cleaned_data['batt_tu_rab']:
        args_str += ' --tu01_rabbit '
    if form.cleaned_data['batt_tu_ab']:
        args_str += ' --tu01_alphabit '
    if form.cleaned_data['batt_tu_bab']:
        args_str += ' --tu01_blockalphabit '

    if form.cleaned_data['email'] != '':
        args_str += ' --email {} '.format(form.cleaned_data['email'])

    args_str += ' --name \'{}\' --cfg \'{}\' --file \'{}\' ' \
        .format(form.cleaned_data['exp_name'], cfg_file_path, in_file_path)

    with open(os.devnull, 'w') as f_null:
        subprocess.call(shlex.split(args_str),
                        stdout=f_null, stderr=subprocess.STDOUT)

    # Remove files on the server
    os.remove(in_file_path)
    os.remove(cfg_file_path)


# Create your views here.
def index(request):
    if request.method != 'POST':
        return render(request, 'SubmitExperiment/index.html', {'form': ExperimentForm()})
    else:
        form = ExperimentForm(request.POST, request.FILES)
        if form.is_valid():
            in_file = request.FILES['in_file']

            if form.cleaned_data['default_cfg']:
                raise NotImplemented('wait for implementation')
            elif form.cleaned_data['choose_cfg'] != '':
                cfg = PredefinedConfiguration.objects.get(id=form.cleaned_data['choose_cfg'])
                cfg_file = cfg.cfg_file
            else:
                cfg_file = request.FILES['own_cfg']

            fs = FileSystemStorage()
            in_file_path = fs.path(fs.save(in_file.name, in_file))
            cfg_file_path = fs.path(fs.save(cfg_file.name, cfg_file))

            try:
                _thread.start_new_thread(submit_experiment,
                                         (form, in_file_path, cfg_file_path))
            except BaseException as e:
                print('wtf: {}'.format(e))

            ctx = {
                'messages': ['Everything is okay'],
                'form': ExperimentForm(),
            }
        else:
            ctx = {
                'errors': ['Something shitty happened.'],
                'form': form,
            }
        return render(request, 'SubmitExperiment/index.html', ctx)
