from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render


def objectIndex(request):
    return render(request, 'objectrecogMain.html')
