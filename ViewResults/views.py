from django.http import Http404
from django.shortcuts import render, reverse
from django.db import connections
from .rtt_db_objects import *
from .rtt_paginator import *
from .forms import FilterExperimentsForm
from django.utils.dateparse import parse_datetime

import logging
logger = logging.getLogger(__name__)


def get_auth_error(request):
    if not request.user.is_authenticated:
        return render(request, 'access_denied.html')

# Create your views here.
def index(request):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    if request.method != 'POST':
        # Filling form object from url parameters
        args = {
            'name': request.GET.get('name', None),
            'sha256': request.GET.get('sha256', None),
            'only_own': request.GET.get('only_own', False),
            'created_from': parse_datetime(request.GET.get('created_from', '')),
            'created_to': parse_datetime(request.GET.get('created_to', ''))
        }
        form = FilterExperimentsForm(args)
    else:
        # Filling form object from posted form
        form = FilterExperimentsForm(request.POST)

    c = connections['rtt-database']
    if not form.is_valid():
        ctx = {
            'paginator': RTTPaginator(request, c, Experiment),
            'form': form
        }
        return render(request, 'ViewResults/index.html', ctx)

    if form.cleaned_data['only_own'] and request.user.is_authenticated:
        email = request.user.email
    else:
        email = None

    object_list = Experiment.get_all_filtered(
        c,
        name=form.cleaned_data['name'],
        sha256=form.cleaned_data['sha256'],
        created_from=form.cleaned_data['created_from'],
        created_to=form.cleaned_data['created_to'],
        email=email,
    )

    ctx = {
        'paginator': RTTPaginator(request, c, Experiment,
                                  object_list=object_list,
                                  url_args=form.as_url_args()),
        'form': form,
    }
    return render(request, 'ViewResults/index.html', ctx)


def experiment(request, experiment_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    c = connections['rtt-database']
    exp = Experiment.get_by_id(c, experiment_id)
    if not exp:
        raise Http404("No such experiment.")

    battery_list = Battery.get_by_experiment_id(c, exp.id)
    battery_list.sort(key=lambda x: x.name)
    ctx = {
        'exp': exp,
        'battery_list': battery_list
    }
    return render(request, 'ViewResults/experiment.html', ctx)


def battery(request, battery_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    c = connections['rtt-database']
    batt = Battery.get_by_id(c, battery_id)
    if not batt:
        raise Http404("No such battery.")

    test_list = Test.get_by_battery_id(c, battery_id)
    for t in test_list:
        t.variant_count = Variant.get_by_test_id_count(c, t.id)

    ctx = {
        'batt': batt,
        'experiment_name': Experiment.get_by_id(c, batt.experiment_id).name,
        'test_list': test_list,
        'battery_error_list': BatteryError.get_by_battery_id(c, battery_id),
        'battery_warning_list': BatteryWarning.get_by_battery_id(c, battery_id)
    }
    return render(request, 'ViewResults/battery.html', ctx)


def test(request, test_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    c = connections['rtt-database']
    tst = Test.get_by_id(c, test_id)
    if not tst:
        raise Http404("No such test.")

    variant_list = Variant.get_by_test_id(c, test_id)
    ctx = {
        'tst': tst,
        'battery_name': Battery.get_by_id(c, tst.battery_id).name,
        'variant_list': variant_list
    }

    if len(variant_list) == 1:
        var = variant_list[0]
        subtest_list = Subtest.get_by_variant_id(c, var.id)
        ctx['subtest_list'] = subtest_list
        ctx['variant_warning_list'] = VariantWarning.get_by_variant_id(c, var.id)
        ctx['variant_error_list'] = VariantError.get_by_variant_id(c, var.id)
        ctx['variant_stderr_list'] = VariantStdErr.get_by_variant_id(c, var.id)

        if len(subtest_list) == 1:
            sub = subtest_list[0]
            ctx['test_parameter_list'] = TestParameter.get_by_subtest_id(c, sub.id)
            ctx['statistic_list'] = Statistic.get_by_subtest_id(c, sub.id)
            ctx['p_value_list'] = PValue.get_by_subtest_id(c, sub.id)

        else:
            for s in subtest_list:
                s.p_val_count = PValue.get_by_subtest_id_count(c, s.id)
                s.statistic_list = Statistic.get_by_subtest_id(c, s.id)

    else:
        for v in variant_list:
            v.result = Variant.get_result(c, v.id)
            v.subtest_list = Subtest.get_by_variant_id(c, v.id)
            for s in v.subtest_list:
                s.statistic_list = Statistic.get_by_subtest_id(c, s.id)

            v.subtest_count = Subtest.get_by_variant_id_count(c, v.id)

    return render(request, 'ViewResults/test.html', ctx)


def variant(request, variant_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    c = connections['rtt-database']
    var = Variant.get_by_id(c, variant_id)
    if not var:
        raise Http404("No such variant.")

    subtest_list = Subtest.get_by_variant_id(c, variant_id)
    ctx = {
        'var': var,
        'test_name': Test.get_by_id(c, var.test_id).name,
        'variant_error_list': VariantError.get_by_variant_id(c, variant_id),
        'variant_warning_list': VariantWarning.get_by_variant_id(c, variant_id),
        'variant_stderr_list': VariantStdErr.get_by_variant_id(c, variant_id),
        'user_setting_list': UserSetting.get_by_variant_id(c, variant_id),
        'subtest_list': subtest_list
    }

    if len(subtest_list) == 1:
        sub = subtest_list[0]
        ctx['test_parameter_list'] = TestParameter.get_by_subtest_id(c, sub.id)
        ctx['statistic_list'] = Statistic.get_by_subtest_id(c, sub.id)
        ctx['p_value_list'] = PValue.get_by_subtest_id(c, sub.id)

    else:
        for s in subtest_list:
            s.p_val_count = PValue.get_by_subtest_id_count(c, s.id)
            s.statistic_list = Statistic.get_by_subtest_id(c, s.id)

    return render(request, 'ViewResults/variant.html', ctx)


def subtest(request, subtest_id):
    auth_error = get_auth_error(request)
    if auth_error is not None:
        return auth_error

    c = connections['rtt-database']
    sub = Subtest.get_by_id(c, subtest_id)
    if not sub:
        raise Http404("No such subtest.")

    var = Variant.get_by_id(c, sub.variant_id)

    ctx = {
        'sub': sub,
        'var_idx': var.variant_index,
        'test_name': Test.get_by_id(c, var.test_id).name,
        'test_parameter_list': TestParameter.get_by_subtest_id(c, subtest_id),
        'statistic_list': Statistic.get_by_subtest_id(c, subtest_id),
        'p_value_list': PValue.get_by_subtest_id(c, subtest_id)
    }
    return render(request, 'ViewResults/subtest.html', ctx)
