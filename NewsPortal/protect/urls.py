from django.urls import path
from .views import IndexView

# перенаправляемся на единственное представление IndexView, которое описано в соответствующем файле views.py
urlpatterns = [
    path('account/profile/', IndexView.as_view()),
]