# Создание фильтра

from django.template import Library
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter


register = Library()


# Фильтер
@register.filter(name='currency', is_safe=True)
def currency(value, name='rub.'):
    return '%1.2f %s' % (value, name)


# register.filter('currency', currency)


# Объявление тега
@register.simple_tag
def lst(sep, *args):
    return mark_safe(f'{sep.join(args)} (len=<strong>{len(args)}</strong>)')


# Шаблонный тег
@register.inclusion_tag('tags/ulist.html')
def ulist(*args):
    return {'items': args}
