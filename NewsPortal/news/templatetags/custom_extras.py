from django import template

register = template.Library()


# Реализуйте фильтр, который заменяет все буквы кроме первой и последней на «*» у слов из списка «нежелательных».
# Предполагается, что в качестве аргумента гарантированно передается текст, и слова разделены пробелами.
# Можно считать, что запрещенные слова находятся в списке forbidden_words.


@register.filter(name='my_filter')  # Оборачиваем функцию в декоратор фильтра
def my_filter(value):
    forbidden_words = ['слово']  # список нежелательных слов
    text = value.split()  # разбиваем текст на слова
    result = []  # переменная для вывода результата
    # в цикле проходимся по каждому слову в тексте
    for word in text:
        if word.lower() in forbidden_words:  # если слово в списке нежелательных
            result.append(word[0] + "*"*(len(word)-2) + word[-1])  # меняем слово и добавляем в результат
        else:
            result.append(word)  # иначе просто добавляем слово не меняя
    return " ".join(result)

