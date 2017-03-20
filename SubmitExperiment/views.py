from django.shortcuts import render, redirect
from django.db import connections
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ExperimentForm


# Create your views here.
def index(request):
    form = ExperimentForm()
    return render(request, 'SubmitExperiment/index.html', {'form': form})


def submit(request):
    if request.method == 'GET':
        return redirect('/SubmitExperiment')
    else:
        form = ExperimentForm(request.POST, request.FILES)
        if form.is_valid():
            ctx = {
                'messages': ['Everything is okay.'],
                'form': ExperimentForm()
            }
        else:
            ctx = {
                'errors': ['Something shitty happened.'],
                'form': form
            }
        return render(request, 'SubmitExperiment/index.html', ctx)
