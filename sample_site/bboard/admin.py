from django.contrib import admin
from django.urls import reverse

from .models import Bb, Rubric, Img
from django.db.models import F


# Уменьшение цен X2
def discount(modeladmin, request, queryset):
    f = F('price')
    for rec in queryset:
        rec.price = f / 2
        rec.save()
    modeladmin.message_user(request, 'Action complete')


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


# Декоратор - редактор
# @admin.register(Bb)
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
    # Радио кнопки вместо списка с рубриками
    radio_fields = {'rubric': admin.VERTICAL}

    # Создание слага из заголовка
    # prepopulated_fields = {'slug': ('title',)}

    # Гиперссыдка на запись модели(Смотреть на сайте)
    def view_on_site(self, rec):
        return reverse('detail', kwargs={'pk': rec.pk})

    # Регестрация действий
    actions = (discount,)


# Встроенный редактор
# Обслуживание модели Bb и вывод объявлений из текущей рубрики
class BbInline(admin.StackedInline):
    model = Bb

    # 8 Форм при создании и 3 при правке
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 3
        else:
            return 8


# Модель рубрик
class RubricAdmin(admin.ModelAdmin):
    inlines = [BbInline]

    # Вывод набора форм только на странице добавления
    def get_inlines(self, request, obj):
        if obj:
            return ()
        else:
            return (BbInline,)


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric, RubricAdmin)
admin.site.register(Img)

# Название функции discount()
discount.short_description = 'Reduce the price by half'
