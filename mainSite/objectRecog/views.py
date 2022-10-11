from django.http import HttpResponse
from django.shortcuts import render
import requests


def objectIndex(request):
    return render(request, 'objectrecogMain.html')

def kakaoApi(request):
  url = "https://1f000b02-5fac-4dcc-9c12-b6e09a06d288.api.kr-central-1.kakaoi.io/ai/vision/24a42b80c90a4df8934dbfada31faa4d"
  files=[
    ('image',('11.png', open('objectRecog/11.png', 'rb'),'image/png'))
  ]
  
  headers = {
    'x-api-key': 'c5931d5912f0137ea003419c3ee4de6b',
    # 'Content-Type': 'multipart/form-data; boundary=<calculated when request is sent>'
  }
  response = requests.request("POST", url, headers=headers, files=files)
  print(response.json())
  return render(request, 'objectrecogMain.html')