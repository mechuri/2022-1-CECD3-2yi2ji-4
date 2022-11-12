from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
import speech_recognition as sr

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
  json_object = json.loads(response.text)['result']
  result = []
  for i in range(len(json_object)):
    result.append({'id': i, 'position':(json_object[i]['x'], json_object[i]['y'], json_object[i]['x']+json_object[i]['w'], json_object[i]['y']+json_object[i]['h']*1.5)})
  return render(request, 'objectrecogMain.html', {"result": result})

def sttFileApi(request):
  AUDIO_FILE = "objectRecog/hello.wav"
  r = sr.Recognizer()
  with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # 전체 audio file 읽기

  try:
    print("Google Speech Recognition thinks you said : " + r.recognize_google(audio, language='ko'))
  except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

def sttMicApi(request):
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

  # 구글 웹 음성 API로 인식하기 (하루에 제한 50회)
  try:
    print("Google Speech Recognition thinks you said : " + r.recognize_google(audio, language='ko'))
  except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

  with open("microphone-results.wav", "wb") as f:
    f.write(audio.get_wav_data())
  return render(request, 'objectrecogMain.html')