from django.contrib import admin

from .models import Bb


# Свои параметры представления модели
class BbAdmin(admin.ModelAdmin):
    # Последовательность имён полей, которые должны выводиться в списке записей
    list_display = ('title', 'content', 'price', 'published')
    # Последовательность имён полей, которые должны быть преобразованы в гиперссылки, ведущие на страницу правки записи
    list_display_links = ('title', 'content')
    # Последовательность имён полей, по которым должна выполняться фильтрация
    search_fields = ('title', 'content')


admin.site.register(Bb, BbAdmin)
