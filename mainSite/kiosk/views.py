from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from django.conf import settings
import base64

def index(request):
    return render(request, 'kioskMain.html')

def upload(request):
  data = request.POST.__getitem__('data')
  data = data[22:]
  path = str(settings.MEDIA_ROOT)
  filename = 'image.png'
  image = open(path+'/'+filename, "wb")
  image.write(base64.b64decode(data))
  image.close()
  # answer = {'filename' : filename}
  return render(request, 'kioskMain.html')
