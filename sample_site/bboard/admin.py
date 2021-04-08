from django.contrib import admin

from .models import Bb, Rubric, Img


# Фильтрация объявлений по цене
class PriceListFilter(admin.SimpleListFilter):
    title = 'Price category'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Low price'),
            ('medium', 'Medium price'),
            ('high', 'High price'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=500)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=500, price__lte=5000)
        elif self.value() == 'high':
            return queryset.filter(price__gt=5000)


# Свои параметры представления модели
class BbAdmin(admin.ModelAdmin):
    # Последовательность имён полей, которые должны выводиться в списке записей
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    # Последовательность имён полей, которые должны быть преобразованы в гиперссылки, ведущие на страницу правки записи
    list_display_links = ('title', 'content')
    # Последовательность имён полей, по которым должна выполняться фильтрация
    search_fields = ('title', 'content')
    # Быстрая фильтрация(по цене), появление справа списка
    list_filter = (PriceListFilter,)
    # Быстрая фильтрация по датам
    date_hierarchy = 'published'
    # Вывод вместо пустого значения поля
    empty_value_display = '---'

    # Рубрика - Добавить можно, а исправить нельзя
    def get_fields(self, request, obj=None):
        f = ['title', 'content', 'price']
        if not obj:
            f.append('rubric')
        return f

    # Только для чтения
    readonly_fields = ('title', 'published')


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
admin.site.register(Img)
