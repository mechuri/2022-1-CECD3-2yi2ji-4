from django.urls import path

from . import views

app_name = "kiosk" # 앱 이름 설정
urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
]