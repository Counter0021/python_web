# Обработчик контекста, добавляющий список рубрик в контекст шаблона
from .models import Rubric


def rubrics(request):
    return {'rubrics': Rubric.objects.all()}
