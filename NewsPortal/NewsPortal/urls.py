"""NewsPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # адрес админки
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),

    # подключаем все адреса из файла urls, который создан в приложении news
    # и добавляем их к posts/
    path('posts/', include('news.urls')),

    path('', include('protect.urls')),

    # перенаправление на ‘account/’ для всех URL, которые будут управляться подключенным пакетом
    path('account/', include('allauth.urls')),
    # чтобы использовать этот пакет без дополнительных настроек как решение «из коробки»
    # достаточно написать базовый шаблон, который будет использовать этот пакет (templates/sign/base.html)

    # подключаем все адреса из файла urls, который создан в приложении sign
    # и добавляем их к sign/
    path('sign/', include('sign.urls')),
]
