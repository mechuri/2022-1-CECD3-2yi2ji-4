from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render


def settingIndex(request):
    return render(request, 'settingMain.html')
