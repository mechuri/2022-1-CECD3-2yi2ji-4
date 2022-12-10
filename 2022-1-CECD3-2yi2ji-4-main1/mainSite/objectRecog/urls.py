from django.urls import path

from . import views
from django.conf import settings 
from django.conf.urls.static import static

app_name = "object"
urlpatterns = [
  path('', views.barcode, name='barcode'),
  path('send/', views.send, name="send"),
  # path('', views.objectIndex, name='objectIndex'),
  path('kakaoApi/', views.kakaoApi, name="kakaoApi"),
  path('sttFileApi/', views.sttFileApi, name="sttFileApi"),
  path('sttMicApi/', views.sttMicApi, name="sttMicApi"),
  path('ttsApi/', views.ttsApi, name="ttsApi"),
  path('roi/', views.roi, name="roi"),
  path('roiResult/', views.roiResult, name="roiResult"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)