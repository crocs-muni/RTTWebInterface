from django.shortcuts import render
from django.shortcuts import render
from django.db import connections
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.
def index(request):
    return render(request, 'SubmitExperiment/index.html')


def submit(request):
    print('dummy')
    return render(request, 'SubmitExperiment/index.html')


def print_stuff(request):
    try:
        text = ""
        file = request.FILES['my_file']
        # with open("file.txt", "wb") as f:
        #     for chunk in file.chunks():
        #         f.write(chunk)
        for chunk in file.chunks():
            text += chunk.decode()

        ctx = {
            'text': text,
        }
    except BaseException as e:
        ctx = {
            'error': str(e),
        }
    """
    try:
        text = request.POST['itext']
        ctx = {
            'text': text,
        }
    except KeyError as e:
        ctx = {
            'error': str(e)
        }
    """

    return render(request, 'SubmitExperiment/print_stuff.html', ctx)
