"""
В данном файле прописывается логика приложения.
Суть представления(views) в джанго - это запрос ин-ии из модели в файле models и
передача ее в шаблон(templates)

После создания представлений, нужно указать адреса, по которым будут доступны представления.
Для настройки адресов используется файл "urls.py" но не тот, который лежит в проекте, а тот
что нужно создать в приложении и указать на него ссылкой из основного файла.

Django поддерживает несколько разных видов представлений:
1) Class-based views — представления, организованные в виде классов.
2) Generic class-based views — часто используемые представления, которые Django предлагает в виде решения «из коробки».
   Они реализуют в первую очередь функционал CRUD (Create Read Update Delete).
3) Function-based views — представления в виде функций.

"""
from django.shortcuts import render, reverse, redirect
# импорт дженериков для представлений.
# дженерики - это элементы, которые позволяют визуализировать ин-ию из БД в браузере, при помощи HTML
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

# Импорт пользовательских элементов:
# модели - передают ин-ию из БД
from .models import Post, Category, CategorySubscribers
# фильтры - прописываются в файле filters.py
# используются для отбора объектов по каким то критериям
from .filters import PostFilter
# формы - прописываются в файле forms.py
# используются для создания форм в браузере по модели
from .forms import PostForm
# Задача отправки письма подписчикам при добавлении статьи в выбранной категории
from .tasks import email_task


# Класс-представление для отображения списка постов
# Унаследован от базового представления"ListView"
class PostList(ListView):
    # указываем имя модели, которая будет использоваться
    # для отображения и реализации логики
    model = Post
    # указываем имя шаблона, то есть html файла,
    # который будет использоваться для визуализации
    template_name = 'news/posts.html'
    # имя, которое будет использоваться для передачи переменных в шаблон
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('-id')
    ordering = ['-id']  # задаем последовательность отображения по id
    paginate_by = 10  # задаем кол-во отображаемых объектов на странице


# Представление, созданное для поиска объектов по фильтрам
class PostsSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'posts_search'
    ordering = ['-time_of_creation']

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон.
    # В возвращаемом словаре context будут храниться все переменные.
    # Ключи этого словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context


# представление для отображения деталей объекта (публикации)
class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    # получение информации об объекте из БД
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует также.
        # Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


# представление для создания объекта.
# наследуемся от миксинов авторизации и разрешения доступа, а так же от стандартного представления
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'news/post_add.html'  # указываем имя шаблона
    form_class = PostForm  # указываем класс формы, созданный в файле forms.py
    permission_required = ('news.add_post',)  # создание разрешения на создание


# класс-представление для редактирования объекта
# унаследован от миксинов авторизации и разрешения,
# чтобы редактировать объект, нужно авторизоваться и иметь доступ
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    # указываем шаблон
    template_name = 'news/post_add.html'
    # форм класс нужен, чтобы получать доступ к форме через метод POST
    form_class = PostForm
    permission_required = ('news.change_post',)  # создание разрешения на редактирование

# !!!! редактирование и создание поста осуществляется в одном и том же шаблоне news/post_add.html.
# Для этого достаточно просто прописать класс формы в атрибутах класса (form_class = PostForm), не меняя при этом шаблон.

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте из БД, который мы собираемся редактировать
    def get_object(self, **kwargs):
        # выдергиваем первичный ключ
        id = self.kwargs.get('pk')
        # возвращаем объект по выдернутому id
        return Post.objects.get(pk=id)


# класс-представление для удаления объекта
# для использования этого представления нужно иметь право доступа и быть авторизованным
# за это отвечаю миксины
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'  # указываем шаблон для отображения
    permission_required = ('news.delete_post',)  # создание разрешения на удаление
    queryset = Post.objects.all()  # получение ин-ии об объекте из БД через запрос
    success_url = '/posts/'  # путь, по которому мы перейдем после удаления поста


# класс-представление для списка категорий
# унаследован от стандартного представления
class CategoryList(ListView):
    model = Category  # указываем модель из которой берем объекты
    template_name = 'news/category_list.html'  # указываем имя шаблона, в котором написан html для отображения объектов модели
    context_object_name = 'categories'  # имя переменной, под которым будет передаваться объект в шаблон


# класс-представление для отображения списка категорий
# унаследован от стандартного представления
class CategoryDetail(DetailView):
    # указываем имя шаблона
    template_name = 'news/category_subscription.html'
    # указываем модель(таблицу базы данных)
    model = Category

    # для отображения кнопок подписки (если не подписан: кнопка подписки - видима, и наоборот)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # общаемся к содержимому контекста нашего представления
        category_id = self.kwargs.get('pk')  # получаем ИД поста (выдергиваем из нашего объекта из модели Категория)
        # формируем запрос, на выходе получим список имен пользователей subscribers__username, которые находятся
        # в подписчиках данной группы, либо не находятся
        category_subscribers = Category.objects.filter(pk=category_id).values("subscribers__username")
        # Добавляем новую контекстную переменную на нашу страницу, выдает либо правду, либо ложь, в зависимости от
        # нахождения нашего пользователя в группе подписчиков subscribers
        context['is_not_subscribe'] = not category_subscribers.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = category_subscribers.filter(subscribers__username=self.request.user).exists()
        return context


# функция-представление обернутая в декоратор
# для добавления пользователя в список подписчиков
# (5)
@login_required
def add_subscribe(request, **kwargs):
    # получаем первичный ключ выбранной категории
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    # добавляем в выбранную категорию, в поле "подписчики" пользователя, который авторизован и делает запрос
    Category.objects.get(pk=pk).subscribers.add(request.user)
    # возвращаемся на страницу со списком категорий
    return redirect('/posts/categories')


# функция-представление обернутая в декоратор
# для удаления пользователя из списка подписчиков
@login_required
def del_subscribe(request, **kwargs):
    # получаем первичный ключ выбранной категории
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    # удаляем в выбранной категории, из поля "подписчики" пользователя, который авторизован и делает запрос
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    # возвращаемся на страницу со списком категорий
    return redirect('/posts/categories')


# функция-представление для рассылки писем подписчикам при появлении новой публикации в выбранной категории
# данная функция будет использоваться в файле news/signals.py
def sending_emails_to_subscribers(instance):
    sub_text = instance.text
    sub_title = instance.title
    # получаем нужный объект модели Категория через рк Пост
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).post_category.pk)
    # получаем список подписчиков категории
    subscribers = category.subscribers.all()

    # проходимся по всем подписчикам в списке
    for subscriber in subscribers:
        # создание переменных, которые необходимы для таски
        subscriber_username = subscriber.username
        subscriber_useremail = subscriber.email
        html_content = render_to_string('news/mail.html',
                                        {'user': subscriber,
                                         'title': sub_title,
                                         'text': sub_text[:50],
                                         'post': instance})
        # функция для таски, передаем в нее все что нужно для отправки подписчикам письма
        email_task(subscriber_username, subscriber_useremail, html_content)
    return redirect('/posts/')

# Реализация отправки письма подписчикам при создании нового поста в их категории
# (было реализовано для представления: "PostCreateView")
# def post(self, request, *args, **kwargs):
#     form = PostForm(request.POST)  # поле формы
#     post_category_pk = request.POST['post_category']  # получение первичного ключа категории
#     sub_text = request.POST.get('text')  # выдергиваем поле с текстом из БД
#     sub_title = request.POST.get('title')  # вы дергиваем заголовок из БД
#     # через запрос и выдернутый первичный ключ, получаем категорию из БД
#     post_category = Category.objects.get(pk=post_category_pk)
#     # создаем переменную(список) в котором хранятся все подписчики полученной категории
#     subscribers = post_category.subscribers.all()
#     # получаем адрес хоста и порта (в нашем случае 127.0.0.1:8000), чтоб в дальнейшем указать его в ссылке
#     # в письме, чтоб пользователь мог с письма переходить на наш сайт, на конкретную новость
#     host = request.META.get('HTTP_HOST')
#
#     # валидатор - чтоб данные в форме были корректно введены, без вредоносного кода от хакеров и прочего
#     if form.is_valid():
#         news = form.save(commit=False)
#         news.save()
#
#     # в цикле проходимся по всем подписчикам из списка
#     for subscriber in subscribers:
#         # (6)
#         # html_content = render_to_string(
#         #     'news/mail_sender.html', {'user': subscriber, 'text': sub_text[:50], 'post': news, 'title': sub_title, 'host': host})
#         # указываем шаблон и переменные для отправки в письме
#         html_content = render_to_string(
#             'news/mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': news, 'title': sub_title, 'host': host}
#         )
#
#         # (7)
#         msg = EmailMultiAlternatives(
#             # Заголовок письма, тема письма
#             subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
#             # Наполнение письма
#             body=f'{sub_text[:50]}',
#             # От кого письмо (должно совпадать с реальным адресом почты)
#             from_email='kalosha21541@yandex.ru',
#             # Кому отправлять, конкретные адреса рассылки, берем из переменной, либо можно явно прописать
#             to=[subscriber.email],
#         )
#
#         # прописываем html-шаблон как наполнение письма
#         msg.attach_alternative(html_content, "text/html")
#         # отправляем письмо
#         msg.send()
#     # возвращаемся на страницу с постами
#     return redirect('/posts/')




# (7)
# способ отправки писем с разным содержимым, то есть по мимо текста можно отправить например
# готовую страницу html (шаблон с готовым содержимым как в нашем случае)
#
# (6)
# все что касается отправки писем в Django читать здесь
# https://www.djbook.ru/rel3.0/topics/email.html#mail-admins
# Отправка письма с шаблоном внутри
# Здесь указываем имя нашего шаблона, и что будет в нашем шаблона, то есть передаем все наши переменные
# и их значения в наш шаблон, если не указать явно их, то будут пустые строчки
#
# (5)
# функция подписки пользователя на категорию новости, которую в данный момент читает пользователь
# передаем с нашей странички news_detail.html на которой находится пользователь (представление DetailView)
# через GET запрос информацию в виде значения переменной ?pk={{ post.category.id }}, далее из объекта request
# через метод GET.get('pk') выдираем ее значение (число) и используем для поиска в модели категории нужной
# категории. С помощью метода add(request.user) добавляем нового пользователя в поле подписоты subscribers на
# рассылку, добавляется связь многие-ко-многим в промежуточной таблице category_subscribers
# (содержит ид записи, ид категории, ид юзера)

