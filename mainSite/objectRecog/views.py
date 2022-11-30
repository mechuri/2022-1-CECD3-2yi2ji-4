from django.shortcuts import render
import requests
import json
import speech_recognition as sr
import pytesseract
import re
from PIL import Image
from django.http import HttpResponse
import pyttsx3
import cv2
import numpy as np
from gtts import gTTS


pytesseract.pytesseract.tesseract_cdm = "objectRecog/tesseract.exe"


def objectIndex(request):
    return render(request, 'objectrecogMain.html')


def kakaoApi(request):

    # kakao 음식 영역 구분 START
    url = "https://1f000b02-5fac-4dcc-9c12-b6e09a06d288.api.kr-central-1.kakaoi.io/ai/vision/24a42b80c90a4df8934dbfada31faa4d"

    imgname = 'image.png'
    imgfile = Image.open(f"./mainSite/media/{imgname}")

    files = [
        ('image', (f'{imgname}', open(f'./mainSite/media/{imgname}', 'rb'), 'image/png'))
    ]

    headers = {
        'x-api-key': 'c5931d5912f0137ea003419c3ee4de6b',
        # 'Content-Type': 'multipart/form-data; boundary=<calculated when request is sent>'
    }
    response = requests.request("POST", url, headers=headers, files=files)
    json_object = json.loads(response.text)['result']
    result = []

    height = []
    for i in range(len(json_object)):
        height.append(json_object[i]['h'])
    max_height = max(height)   

    for i in range(len(json_object)):

        leftX = json_object[i]['x']
        leftY = json_object[i]['y']
        rightX = json_object[i]['x'] + json_object[i]['w']
        rightY = json_object[i]['y'] + max_height * 2

        # 음식영역에 따른 이미지 crop
        cropped_img = imgfile.crop((leftX, leftY, rightX, rightY))
        cropped_img.show()

        # crop 된 이미지를 tesseract ocr 처리
        result_ocr = pytesseract.image_to_string(cropped_img, lang='kor')

        # ocr 결과에서 공백 제거하고 한글과 숫자 구분
        result_no_space = re.sub(r"[\s]", "", result_ocr)
        final = result_no_space.rstrip('원')
        title = re.sub(r"[^\uAC00-\uD7A3]", "", final)
        price = re.sub(r"[^0-9]", "", final)
        print("title : " + title + ", price : " + price)

        result.append({'id': i,
                       'left-x': leftX,
                       'left-y': leftY,
                       'right-x': rightX,
                       'right-y': rightY,
                       'title': title,
                       'price': price},
                      )

    print(result)

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
    return render(request, 'objectrecogMain.html')

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
    return render(request, 'objectrecogMain.html', {"result" : r.recognize_google(audio, language='ko')})


def ttsApi(request):
    result = [{'id': 0, 'position': (786, 547, 1004, 871.0), 'title': '멸치김밥', 'price': '4500'}
        , {'id': 1, 'position': (57, 198, 286, 538.5), 'title': '치즈김밥', 'price': '4500'}
        , {'id': 2, 'position': (422, 199, 645, 536.5), 'title': '치즈김밥', 'price': '4500'}
        , {'id': 3, 'position': (64, 903, 290, 1246.5), 'title': '치즈김밥', 'price': '4500'}
        , {'id': 4, 'position': (54, 545, 298, 908.0), 'title': '치즈김밥', 'price': '4500'}
        , {'id': 5, 'position': (418, 545, 667, 908.0), 'title': '치즈김밥', 'price': '4500'}
        , {'id': 6, 'position': (768, 901, 1008, 1252.0), 'title': '치즈김밥', 'price': '4500'}
        , {'id': 7, 'position': (769, 193, 1010, 547.0), 'title': '치즈김밥', 'price': '4500'}
        , {'id': 8, 'position': (380, 879, 713, 1290.0), 'title': '치즈김밥', 'price': '4500'}
        , {'id': 9, 'position': (847, 1035, 955, 1173.0), 'title': '치즈김밥', 'price': '4500'}]
    count = 0
    for i in range(len(result)):
        if result[i]['title'] == "멸치김밥":
            title = result[i]['title']
            price = result[i]['price'] + '원'
            count += 1
    if count == 0:
        title = '검색결과가 없습니다.'
        price = '  다른 메뉴를 말씀해주세요.'
    # tts = gTTS(text=title+price, lang='ko')
    # tts.save('result.wav')
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.say(title + price)
    engine.runAndWait()
    return render(request, 'objectrecogMain.html', {"result": title + price})


def roi(request):
    img = cv2.imread('objectRecog/image.png')

    (x, y), (w, h) = (54, 545), (244, 242)

    roi = img[y:y + h, x:x + w]

    cv2.rectangle(roi, (0, 0), (h - 1, w - 1), (0, 255, 0))
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return render(request, 'objectrecogMain.html')