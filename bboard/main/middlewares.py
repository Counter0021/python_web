from .models import SubRubric


# Добавляем рубрики в контекст шаблона
def bboard_context_processor(request):
    context = {}
    context['rubrics'] = SubRubric.objects.all()
    return context
