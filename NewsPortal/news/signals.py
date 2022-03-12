# Импортируем отправку писем
from django.core.mail import EmailMultiAlternatives
# импортируем сигнал, который будет срабатывать после сохранения объекта в базу данных
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.shortcuts import redirect
from django.template.loader import render_to_string

# Импорт пользовательских элементов:
# модели - передают ин-ию из БД
from .models import Post, Category
from .views import sending_emails_to_subscribers


# создание сигнала
# оборачиваем в декоратор и выбираем тип сигнала и модель
@receiver(post_save, sender=Post)
# описываем функцию сигнала и передаем экземпляр модели
def send_emails_on_signal(sender, created, instance, **kwargs):
    # запускаем функцию представление
    sending_emails_to_subscribers(instance)

# Функция обработчик для сигнала "post_save"
# создаём функцию обработчик с параметрами под регистрацию сигнала
# запускает выполнение кода при каком-либо действии пользователя, в нашем случае -
# сохранение в БД модели Post записи
# @receiver(post_save, sender=Post)
# def send_sub_mail(sender, instance, created, **kwargs):
#     global subscriber
#     sub_title = instance.title
#     sub_text = instance.text
#     category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).post_category.pk)
#     subscribers = category.subscribers.all()
#     post = instance
#
#     for subscriber in subscribers:
#         html_content = render_to_string(
#             'news/mail.html', {'user': subscriber, 'title': sub_title, 'text': sub_text[:50], 'post': post})
#
#         msg = EmailMultiAlternatives(
#             subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
#             from_email='kalosha21541@yandex.ru',
#             to=[subscriber.email]
#         )
#         msg.attach_alternative(html_content, 'text/html')
#         msg.send()
#     return redirect('/posts/')


