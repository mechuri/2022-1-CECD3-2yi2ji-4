from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import os
from PIL import Image
import pytesseract
import json
import re
import requests

pytesseract.pytesseract.tesseract_cdm = "tesseractocr/tesseract.exe"


def ocr_upload(request):
    context = {}
    context['menutitle'] = 'OCR READ'

    imgname = ''
    resulttext = ''

    if 'uploadfile' in request.FILES:
        uploadfile = request.FILES.get('uploadfile', '')

        if uploadfile != '':
            name_old = uploadfile.name
            name_ext = os.path.splitext(name_old)[1]

            fs = FileSystemStorage(location='static/source')
            imgname = fs.save(f"src-{name_old}", uploadfile)

            imgfile = Image.open(f"./static/source/{imgname}")

            # json_data = '[{"id": 0, "left-x": 1066, "left-y": 1522, "right-x": 1485, "right-y": 1832.5}, {"id": 1, "left-x": 597, "left-y": 1009, "right-x": 939, "right-y": 1229.5}, {"id": 2, "left-x": 109, "left-y": 1600, "right-x": 427, "right-y": 1802.5}, {"id": 3, "left-x": 602, "left-y": 1092, "right-x": 931, "right-y": 1270.5}, {"id": 4, "left-x": 96, "left-y": 483, "right-x": 457, "right-y": 816.0}, {"id": 5, "left-x": 1097, "left-y": 1073, "right-x": 1429, "right-y": 1281.5}, {"id": 6, "left-x": 135, "left-y": 1097, "right-x": 465, "right-y": 1254.5}, {"id": 7, "left-x": 561, "left-y": 492, "right-x": 999, "right-y": 810.0}, {"id": 8, "left-x": 1092, "left-y": 461, "right-x": 1441, "right-y": 650.0}, {"id": 9, "left-x": 585, "left-y": 1522, "right-x": 933, "right-y": 1721.5}, {"id": 10, "left-x": 587, "left-y": 1604, "right-x": 921, "right-y": 1781.0}, {"id": 11, "left-x": 1098, "left-y": 575, "right-x": 1414, "right-y": 755.0}, {"id": 12, "left-x": 108, "left-y": 1514, "right-x": 440, "right-y": 1685.0}, {"id": 13, "left-x": 132, "left-y": 1013, "right-x": 484, "right-y": 1190.0}]'
            # json_data = '[{"id": 0, "left-x": 786, "left-y": 547, "right-x": 1004, "right-y": 871.0}, {"id": 1, "left-x": 57, "left-y": 198, "right-x": 286, "right-y": 538.5}, {"id": 2, "left-x": 422, "left-y": 199, "right-x": 645, "right-y": 536.5}, {"id": 3, "left-x": 64, "left-y": 903, "right-x": 290, "right-y": 1246.5}, {"id": 4, "left-x": 54, "left-y": 545, "right-x": 298, "right-y": 908.0}, {"id": 5, "left-x": 418, "left-y": 545, "right-x": 667, "right-y": 908.0}, {"id": 6, "left-x": 768, "left-y": 901, "right-x": 1008, "right-y": 1252.0}, {"id": 7, "left-x": 769, "left-y": 193, "right-x": 1010, "right-y": 547.0}, {"id": 8, "left-x": 380, "left-y": 879, "right-x": 713, "right-y": 1290.0}, {"id": 9, "left-x": 847, "left-y": 1035, "right-x": 955, "right-y": 1173.0}]'
            json_data = '[{"id": 0, "left-x": 786, "left-y": 547, "right-x": 1004, "right-y": 871.0, "title": "", "price": ""}, {"id": 2, "left-x": 422, "left-y": 199, "right-x": 645, "right-y": 536.5, "title": "", "price": ""}]'
            # 버거킹맑은고딕
            # json_data = '[{"id": 0, "left-x": 1066, "left-y": 1520, "right-x": 1485, "right-y": 1938}, {"id": 1, "left-x": 596, "left-y": 1009, "right-x": 939, "right-y": 1307}, {"id": 2, "left-x": 109, "left-y": 1600, "right-x": 427, "right-y": 1870}, {"id": 3, "left-x": 96, "left-y": 483, "right-x": 459, "right-y": 929}, {"id": 4, "left-x": 601, "left-y": 1089, "right-x": 932, "right-y": 1333}, {"id": 5, "left-x": 1097, "left-y": 1072, "right-x": 1429, "right-y": 1350}, {"id": 6, "left-x": 134, "left-y": 1096, "right-x": 467, "right-y": 1310}, {"id": 7, "left-x": 561, "left-y": 492, "right-x": 1001, "right-y": 914}, {"id": 8, "left-x": 1092, "left-y": 460, "right-x": 1441, "right-y": 714}, {"id": 9, "left-x": 587, "left-y": 1603, "right-x": 921, "right-y": 1843}, {"id": 10, "left-x": 1098, "left-y": 574, "right-x": 1414, "right-y": 818}, {"id": 11, "left-x": 584, "left-y": 1522, "right-x": 934, "right-y": 1790}, {"id": 12, "left-x": 108, "left-y": 1514, "right-x": 439, "right-y": 1742}, {"id": 13, "left-x": 132, "left-y": 1012, "right-x": 485, "right-y": 1252}]'
            # json_data = '[{"id": 0, "left-x": 181, "left-y": 542, "right-x": 336, "right-y": 1108}, {"id": 1, "left-x": 1235, "left-y": 542, "right-x": 1390, "right-y": 1096}, {"id": 2, "left-x": 176, "left-y": 1533, "right-x": 339, "right-y": 2123}, {"id": 3, "left-x": 704, "left-y": 564, "right-x": 863, "right-y": 1088}, {"id": 4, "left-x": 696, "left-y": 1541, "right-x": 863, "right-y": 2109}, {"id": 5, "left-x": 1236, "left-y": 1543, "right-x": 1390, "right-y": 2123}, {"id": 6, "left-x": 1242, "left-y": 1027, "right-x": 1393, "right-y": 1609}, {"id": 7, "left-x": 698, "left-y": 1024, "right-x": 865, "right-y": 1610}, {"id": 8, "left-x": 156, "left-y": 1070, "right-x": 310, "right-y": 1520}]'

            print(json_data)
            json_ini = json.loads(json_data)
            i = 0

            for data in json_ini:
                id = data['id']
                leftX = data['left-x']
                leftY = data['left-y']
                rightX = data['right-x']
                rightY = data['right-y']
                cropped_img = imgfile.crop((leftX, leftY, rightX, rightY))
                # cropped_img.show()
                result = pytesseract.image_to_string(cropped_img, lang='kor')
                result1 = re.sub(r"[\s]", "", result)
                title = re.sub(r"[^\uAC00-\uD7A3]", "", result1)
                price = re.sub(r"[^0-9]", "", result1)

                data['title'] = title
                data['price'] = price
                print("title : " + title + ", price : " + price)
                i = i + 1


            print(json_ini)

    context['imgname'] = imgname
    context['resulttext'] = resulttext.replace(" ", "")
    return render(request, 'tesseractocr.html', context)


def kakao(request):
    url = "https://1f000b02-5fac-4dcc-9c12-b6e09a06d288.api.kr-central-1.kakaoi.io/ai/vision/24a42b80c90a4df8934dbfada31faa4d"

    imgname = '.png'
    files = [
        ('image', (f'{imgname}', open(f'tesseractocr/{imgname}', 'rb'), 'image/png'))
    ]

    headers = {
        'x-api-key': 'c5931d5912f0137ea003419c3ee4de6b',
        # 'Content-Type': 'multipart/form-data; boundary=<calculated when request is sent>'
    }
    response = requests.request("POST", url, headers=headers, files=files)
    json_object = json.loads(response.text)['result']
    result = []


    for i in range(len(json_object)):
        result.append({'id': i,
                       'left-x': json_object[i]['x'],
                       'left-y': json_object[i]['y'],
                       'right-x': json_object[i]['x'] + json_object[i]['w'],
                       'right-y': json_object[i]['y'] + json_object[i]['h'] * 2}
                      )

    return render(request, 'tesseractocr.html', {"result": result})
