from .models import SubRubric


# Добавляем рубрики в контекст шаблона
def bboard_context_processor(request):
    context = {}
    context['rubrics'] = SubRubric.objects.all()
    # Сохранение страницы и поиска при попытки возврата
    context['keyword'] = ''
    context['all'] = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context
