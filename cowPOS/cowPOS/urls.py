# 全体のURL

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # app_folderにアクセスするURL
    path('AppPOS/', include('AppPOS.urls')),
    # 管理サイトにアクセスするURL
    path('admin/', admin.site.urls)
]
