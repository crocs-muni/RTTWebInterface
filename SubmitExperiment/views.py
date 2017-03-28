from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from .forms import ExperimentForm
from .models import PredefinedConfiguration
from .models import AccessCode

from types import SimpleNamespace
import subprocess
import shlex
import os
import _thread

# Path to submit_experiment executable relative
# to root directory of Django project
SUBMIT_EXPERIMENT_BINARY = 'SubmitExperiment/submit_binary/submit_experiment'


# Checks whether user is authenticated. If he is not,
# access code (if any) is checked. If this function
# returns anything other than None it is rendered
# appropriate error page and authentication failed.
def get_auth_error(request):
    # Is user authenticated?
    if not request.user.is_authenticated:
        # User is not logged in. But maybe he has stored access code in session?
        access_code = request.session.get('access_code', None)
        if access_code is not None:
            # Yup, he has. Let's check it.
            try:
                # Is the code even in the database?
                ac = AccessCode.objects.get(access_code=access_code)
                # Hmm, yes it is. But is it still valid?
                if not ac.is_valid():
                    # No it is not. Get out.
                    return render(request, 'SubmitExperiment/access_code_expired.html')

                # Okay, he has stored correct code that is still valid, let him in.
                return None

            except AccessCode.DoesNotExist:
                # Wrong code, sorry buddy.
                return render(request, 'SubmitExperiment/access_code_bad.html')
        else:
            # Nope, he has not. So kick him out, he has no business here.
            return render(request, 'access_denied.html')
    else:
        # User is logged in, everything is okay.
        return None


def submit_experiment(form, email, in_file_path, cfg_file_path):
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

    if email is not None and len(email) > 0:
        args_str += ' --email {} '.format(email)

    args_str += ' --name \'{}\' --cfg \'{}\' --file \'{}\' ' \
        .format(form.cleaned_data['exp_name'], cfg_file_path, in_file_path)

    with open(os.devnull, 'w') as f_null:
        subprocess.call(shlex.split(args_str),
                        stdout=f_null, stderr=subprocess.STDOUT)

    # Remove files on the server
    os.remove(in_file_path)
    os.remove(cfg_file_path)


# Sole purpose of this view is to save access code into
# session.
# Code will be verified when accessing index (so after redirect)
def gain_access(request, access_code):
    request.session['access_code'] = access_code
    return redirect('SubmitExperiment:index')


# Create your views here.
def index(request):
    # Authentication
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    # Finally process the request
    if request.method != 'POST':
        # GET processing
        # Render the form
        return render(request, 'SubmitExperiment/index.html', {'form': ExperimentForm()})

    # POST processing
    # Validate form and submit experiment
    form = ExperimentForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, 'Submitted form was not valid.')
        messages.info(request, 'Please fix the errors and try again.')
        return render(request, 'SubmitExperiment/index.html', {'form': form})

    # Form is valid here, continue
    in_file = request.FILES['in_file']

    if form.cleaned_data['default_cfg']:
        # Picking default configuration if possible
        config_list = PredefinedConfiguration.objects.all().order_by('required_bytes')
        if len(config_list) == 0:
            raise AssertionError('there are no predefined configurations')

        last_leq_id = None
        for c in config_list:
            if in_file.size >= c.required_bytes:
                last_leq_id = c.id
            else:
                break

        if last_leq_id is None:
            last_leq_id = config_list[0].id
            messages.warning(request, "Provided file is too small for all configurations.")

        chosen_cfg = PredefinedConfiguration.objects.get(id=last_leq_id)
        messages.info(request, "Best possible configuration was chosen and requires {} bytes."
                      .format(chosen_cfg.required_bytes))
        cfg_file = chosen_cfg.cfg_file

    elif form.cleaned_data['choose_cfg'] is not None:
        # User picked one of predefined configurations
        cfg = PredefinedConfiguration.objects.get(id=form.cleaned_data['choose_cfg'].id)
        cfg_file = cfg.cfg_file
        if in_file.size < cfg.required_bytes:
            messages.warning(request, "Your file is smaller than"
                                      "recommended file size for chosen configuration.")
            messages.warning(request, "Recommended file size: {} bytes".format(cfg.required_bytes))
            messages.warning(request, "Size of provided file: {} bytes".format(in_file.size))
    else:
        # User provided his own configuration
        cfg_file = request.FILES['own_cfg']

    fs = FileSystemStorage()
    in_file_path = fs.path(fs.save(in_file.name, in_file))
    cfg_file_path = fs.path(fs.save(cfg_file.name, cfg_file))

    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = form.cleaned_data['author_email']

    try:
        _thread.start_new_thread(submit_experiment,
                                 (form, email, in_file_path, cfg_file_path))
    except BaseException as e:
        print('Could not start a thread: {}'.format(e))

    messages.success(request, 'Experiment {} was created.'.format(form.cleaned_data['exp_name']))
    return redirect('SubmitExperiment:index')
