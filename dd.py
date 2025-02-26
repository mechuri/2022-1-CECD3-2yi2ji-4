from PIL import Image
from imutils.perspective import four_point_transform
from imutils.contours import sort_contours
import matplotlib.pyplot as plt
import pytesseract
import imutils
import cv2
import re
import requests
import numpy as np
import cv2
import os



# path = '/Users/jiwon/Documents/투이투지/3.png'
# #이미지 문자 출력
# img = Image.open(path)
# text = pytesseract.image_to_string(img,lang='kor')
# print(text)

# 이미지 출력
def plt_imshow(title='image', img=None, figsize=(8 ,5)):
    plt.figure(figsize=figsize)
 
    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            titles = []
 
            for i in range(len(img)):
                titles.append(title)
 
        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)
 
            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
 
        plt.show()
    else:
        if len(img.shape) < 3:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
        plt.imshow(rgbImg)
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()


# OCR
#path = 'https://marketplace.canva.com/EAD1R3xvxA4/1/0/1236w/canva-%EA%B2%80%EC%9D%80%EC%83%89-%EC%9E%94-%EC%B9%B5%ED%85%8C%EC%9D%BC-%EB%A9%94%EB%89%B4-peIy1v1nb24.jpg'
path = '/Users/jiwon/Documents/투이투지/7.jpeg'
# image_nparray = np.asarray(bytearray(requests.get(path).content), dtype=np.uint8)
# org_image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR) 
 
# plt_imshow("orignal image", org_image)

org_image = cv2.imread(path)


# options = "--psm 4"
# text = pytesseract.image_to_string(cv2.cvtColor(org_image, cv2.COLOR_BGR2RGB), config=options, lang='kor')
 
# # OCR결과
# print(text)
# print("\n")

# 이미지 처리
gray = cv2.cvtColor(org_image, cv2.COLOR_BGR2GRAY)
(H, W) = gray.shape
 
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 20))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 21))
 
gray = cv2.GaussianBlur(gray, (11, 11), 0)
blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
 
grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
grad = np.absolute(grad)
(minVal, maxVal) = (np.min(grad), np.max(grad))
grad = (grad - minVal) / (maxVal - minVal)
grad = (grad * 255).astype("uint8")
 
grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rectKernel)
thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
close_thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
close_thresh = cv2.erode(close_thresh, None, iterations=2)
 
#plt_imshow(["Original", "Blackhat", "Gradient", "Rect Close", "Square Close"], [org_image, blackhat, grad, thresh, close_thresh], figsize=(16, 10))
plt_imshow(["글자 영역 인식"], [close_thresh], figsize=(16, 10))


cnts = cv2.findContours(close_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sort_contours(cnts, method="top-to-bottom")[0]
 
roi_list = []
roi_title_list = []
 
margin = 10
receipt_grouping = org_image.copy()
 
for c in cnts:
#   print(c)
#   print("\n")
  (x, y, w, h) = cv2.boundingRect(c)
  ar = w // float(h)
  #img2 = cv2.rectangle(receipt_grouping, (x, y), (x + w, y + h), (0,255,0), 2)
  #print(cv2.boundingRect(c))
  color = (255, 0, 0)
  
  #cv2.rectangle(receipt_grouping, (x - margin, y - margin), (x + w + margin, y + h + margin), color, 2)
  #plt_imshow(["g"], [receipt_grouping], figsize=(16, 10))
  #cv2.putText(receipt_grouping, "".join(str(ar)), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

  roi = org_image[y - margin:y + h + margin, x - margin:x + w + margin]
#   roi_list.append(roi)
#   roi_title_list.append("Roi_{}".format(len(roi_list)))
#   print(roi_title_list)
#   gray_roi= cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#   threshold_roi = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  if (bool(roi.any())):
    roi_text = pytesseract.image_to_string(roi,lang='kor')
    if ("원" in roi_text or "00" in roi_text):
        color = (255, 0, 0)
        img2 = cv2.rectangle(receipt_grouping, (x, y), (x + w, y + h), (0,255,0), 2)
        roi = org_image[y - margin:y + h + margin, x - margin:x + w + margin]
        roi_list.append(roi)
        roi_title_list.append("Roi_{}".format(len(roi_list)))
        print(roi_text)

plt_imshow(["글자 영역 표시"], [receipt_grouping], figsize=(16, 10))

#   if ar > 3.0 and ar < 6.5 and (W/2) < x:
#     color = (0, 255, 0)
#     roi = org_image[y - margin:y + h + margin, x - margin:x + w + margin]
#     roi_list.append(roi)
#     roi_title_list.append("Roi_{}".format(len(roi_list)))
#   else:
#     color = (0, 0, 255)
 
#   cv2.rectangle(receipt_grouping, (x - margin, y - margin), (x + w + margin, y + h + margin), color, 2)
#   cv2.putText(receipt_grouping, "".join(str(ar)), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)
  
  #plt_imshow(["Grouping Image"], [receipt_grouping], figsize=(16, 10))
  #plt_imshow(roi_title_list, roi_list, figsize=(16, 10))
 
# for roi in roi_list:
#   gray_roi= cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#   threshold_roi = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#   roi_text = pytesseract.image_to_string(threshold_roi)
#   print(roi_text)
#   print()
#   print(cv2.boundingRect(c))


#   def mergeResize(img, row=300, col=200):
#     IMG_COL = col #66
 
#     # row값에 따른 col값 변경
#     IMG_COL = int((row * IMG_COL)/row)
 
#     IMG_ROW = row
#     border_v = 0
#     border_h = 0
 
#     if (IMG_COL / IMG_ROW) >= (img.shape[0] / img.shape[1]):
#         border_v = int((((IMG_COL / IMG_ROW) * img.shape[1]) - img.shape[0]) / 2)
#     else:
#         border_h = int((((IMG_ROW / IMG_COL) * img.shape[0]) - img.shape[1]) / 2)
#     img = cv2.copyMakeBorder(img, top=border_v, bottom=border_v, left=0, right=border_h + border_h, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))
#     img = cv2.resize(img, (IMG_ROW, IMG_COL))
#     return img


# for idx, roi in enumerate(roi_list):
#   if idx == 0:
#     mergeImg = mergeResize(roi)
#   else:
#     cropImg = mergeResize(roi)
#     mergeImg = np.concatenate((mergeImg, cropImg), axis=0)
    
# threshold_mergeImg = cv2.threshold(mergeImg, 150, 255, cv2.THRESH_BINARY)[1]
# plt_imshow(["Merge Image"], [threshold_mergeImg])
# merge_Img_text = pytesseract.image_to_string(threshold_mergeImg)
# print(merge_Img_text)

