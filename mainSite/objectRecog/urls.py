from django.urls import path

from . import views

urlpatterns = [
  path('', views.objectIndex, name='objectIndex'),
  path('kakaoApi/', views.kakaoApi, name="kakaoApi"),
  path('sttFileApi/', views.sttFileApi, name="sttFileApi"),
  path('sttMicApi/', views.sttMicApi, name="sttMicApi"),
  path('ttsApi/', views.ttsApi, name="ttsApi"),
  path('roi/', views.roi, name="roi"),
  path('roiResult/', views.roiResult, name="roiResult"),
]