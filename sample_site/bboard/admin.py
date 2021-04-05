from django.contrib import admin

from .models import Bb, Rubric, Img


# Свои параметры представления модели
class BbAdmin(admin.ModelAdmin):
    # Последовательность имён полей, которые должны выводиться в списке записей
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    # Последовательность имён полей, которые должны быть преобразованы в гиперссылки, ведущие на страницу правки записи
    list_display_links = ('title', 'content')
    # Последовательность имён полей, по которым должна выполняться фильтрация
    search_fields = ('title', 'content')


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
admin.site.register(Img)

