from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ocr_upload, name='ocr_upload'),
    path('kakao/', views.kakao, name='kakao'),
]
