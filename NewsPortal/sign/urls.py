"""
файл адресов для приложения "sign", которое отвечает за вход/регистрацию пользователей
"""

from django.urls import path
# Импорт представлений из "коробки" для реализации аутентификации
# Для его использования достаточно в файле конфигурации URL
# (приложения sign в этом примере) импортировать его и вставить в urlpatterns:
from django.contrib.auth.views import LoginView, LogoutView

from .views import upgrade_me, not_author


urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),  # указываем шаблон для вывода формы
         name='login'),  # устанавливаем имена для этих URL в целях удобства обращения к ним из шаблонов
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),  # указываем шаблон для вывода формы
         # При выходе с сайта (вспоминаем кнопку, которую мы создали раньше в шаблоне index.html)
         # Django перенаправит пользователя на страницу, указанную в параметре template_name класса LogoutView.
         name='logout'),  # устанавливаем имена для этих URL в целях удобства обращения к ним из шаблонов
    path('upgrade_me/', upgrade_me, name='author'),
    path('not_author/', not_author, name='not_author'),
]