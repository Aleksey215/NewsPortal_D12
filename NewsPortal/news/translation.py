from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions  # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться


# регистрируем наши модели для перевода
@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text', )


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
