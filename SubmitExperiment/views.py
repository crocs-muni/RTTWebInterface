from django.shortcuts import render
from django.shortcuts import render
from django.db import connections


# Create your views here.
def index(request):
    return render(request, 'SubmitExperiment/index.html')
