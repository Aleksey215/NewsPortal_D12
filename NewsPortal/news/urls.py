"""
Данный файл описывает продолжение адреса для конкретного приложения.
То есть главный файл urls.py ссылается на файл news.urls и приписывает в начале адреса: posts/ (например)
после чего начинают действовать адреса, указанные в этом файле в переменной "urlpatterns"
Главный файл забирает все адреса из этого файла, чтобы выстроить полный путь
"""

from django.urls import path
# Импортируем представления, написанные в файле "views.py"
from .views import PostList, PostsSearch, PostDetailView, \
    PostCreateView, PostUpdateView, PostDeleteView, \
    CategoryList, add_subscribe, del_subscribe, CategoryDetail
# Д8 кэширование
from django.views.decorators.cache import cache_page

# создаем список всех url-адресов данного приложения
# мысленно добавляем к каждому адресу: posts/ из главного файла
# в переменной name указываем имя шаблона для визуализации
urlpatterns = [
    # D8 добавил кеширование
    # по пустому адресу мы получаем список публикаций как представление
    path('', cache_page(60)(PostList.as_view()), name='posts'),  # т. к. сам по себе это класс,
    # то нам надо представить этот класс в виде view. Для этого вызываем метод as_view

    # адрес для поиска постов
    path('search/', PostsSearch.as_view(), name='search'),

    # адрес к конкретному объекту по его id или pk
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # адрес для добавления поста
    path('add/', PostCreateView.as_view(), name='post_add'),

    # адрес для редактирования выбранного поста
    path('add/<int:pk>', PostUpdateView.as_view(), name='post_update'),

    # адрес для удаления выбранного поста
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),

    # адрес для просмотра категорий
    # Д8 - кэширование (сохранение представления в кэш на 1 мин)
    # Вывод страницы со списком категорий
    path('categories/', cache_page(60)(CategoryList.as_view()), name='categories'),
    # Страница выбранной категории для подписки/отписки
    path('categories/<int:pk>/', cache_page(60 * 5)(CategoryDetail.as_view()), name='category_subscription'),
    # Функция-представление для подписки на выбранную категорию
    path('categories/<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    # Функция-представление для отписки от выбранной категории
    path('categories/<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
]
