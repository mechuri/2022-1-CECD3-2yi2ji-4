from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import os
from PIL import Image
import pytesseract
import json
import re

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
            json_data = '[{"id": 0, "left-x": 786, "left-y": 547, "right-x": 1004, "right-y": 871.0}, {"id": 1, "left-x": 57, "left-y": 198, "right-x": 286, "right-y": 538.5}, {"id": 2, "left-x": 422, "left-y": 199, "right-x": 645, "right-y": 536.5}, {"id": 3, "left-x": 64, "left-y": 903, "right-x": 290, "right-y": 1246.5}, {"id": 4, "left-x": 54, "left-y": 545, "right-x": 298, "right-y": 908.0}, {"id": 5, "left-x": 418, "left-y": 545, "right-x": 667, "right-y": 908.0}, {"id": 6, "left-x": 768, "left-y": 901, "right-x": 1008, "right-y": 1252.0}, {"id": 7, "left-x": 769, "left-y": 193, "right-x": 1010, "right-y": 547.0}, {"id": 8, "left-x": 380, "left-y": 879, "right-x": 713, "right-y": 1290.0}, {"id": 9, "left-x": 847, "left-y": 1035, "right-x": 955, "right-y": 1173.0}]'

            print("----------------------\n")

            print(json_data)
            json_ini = json.loads(json_data)
            for data in json_ini:
                leftX = data['left-x']
                leftY = data['left-y']
                rightX = data['right-x']
                rightY = data['right-y']
                cropped_img = imgfile.crop((leftX, leftY, rightX, rightY))
                result = pytesseract.image_to_string(cropped_img, lang='kor')
                result1 = re.sub(r"[\s]", "", result)
                title = re.sub(r"[^\uAC00-\uD7A3]", "", result1)
                price = re.sub(r"[^0-9]", "", result1)
                print("title : " + title + ", price : " + price)

            # resulttext = pytesseract.image_to_string(imgfile, lang='kor')
            # print("------- 결과 : " + resulttext + "--------------")

        # cropped_img = imgfile.crop((786, 547, 1004, 871.0))
        # cropped_img.show()

    context['imgname'] = imgname
    context['resulttext'] = resulttext.replace(" ", "")
    return render(request, 'tesseractocr.html', context)
