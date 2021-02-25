from django import template

from recipes.models import BR, DIN, LU

register = template.Library()


@register.filter
def addclass(field, css):
    """Добавляет поле class к input формы"""
    return field.as_widget(attrs={"class": css})


@register.filter
def class_tag(tag):
    """Возвращает необходимое поле class
    для кнопки включения/выключения тега"""
    classes = {
        BR: "badge badge_style_orange",
        LU: "badge badge_style_green",
        DIN: "badge badge_style_purple",
    }
    return classes[tag]
