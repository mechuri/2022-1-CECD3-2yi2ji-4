from django.urls import path
from . import views


app_name = "ocr"
urlpatterns = [
    path('', views.ocrIndex, name='ocrIndex'),
    path('startocr/', views.startocr, name="startocr"),
    path('openocr/', views.startocr, name="openocr"),
    path('webcam_feed', views.webcam_feed, name='webcam_feed'),
]