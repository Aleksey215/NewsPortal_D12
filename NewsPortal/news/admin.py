"""
В данном файле регистрируются модели, чтобы их можно было видеть в админке
"""
from django.contrib import admin
# Импортируем модели, которые нужны нам в админке
from .models import Post, Category, Author, Comment, CategorySubscribers


def like_plus_five(modeladmin, request, queryset):
    # функция накрутки лайков статье
    for posts in queryset:
        posts.rating = posts.rating + 5
        posts.save()


def like_minus_five(modeladmin, request, queryset):
    # функция  скрутки лайков статье
    for posts in queryset:
        posts.rating = posts.rating - 5
        posts.save()


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display - это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('id', 'title', 'post_category', 'view', 'author', 'post_rating',)
    list_filter = ('post_category', 'author')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title',)  # тут всё очень похоже на фильтры из запросов в базу
    actions = [like_plus_five, like_minus_five]  # добавляем действия в список


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class CategorySubscribersAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_categories', 'sub_users')


# регистрируем наши модели
admin.site.register(Post, PostAdmin)  # Не забываем добавить классы
admin.site.register(Category, CategoryAdmin)  # Не забываем добавить классы
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(CategorySubscribers, CategorySubscribersAdmin)  # Не забываем добавить классы

