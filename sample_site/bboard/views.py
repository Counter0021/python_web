from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Bb, Rubric

from .forms import BbForm


# Контроллер класс, для обработки формы
class BbCreateView(CreateView):
    # Путь к файлу шаблона, создающего страницу с формой
    template_name = 'bboard/create.html'
    # Ссылка на класс формы, связанной с моделью
    form_class = BbForm
    # Интернет-адрес для перенаправления после успешного сохранения данных
    success_url = reverse_lazy('index')

    # Вывод перечня рубрик, он формирует контекст шаблона
    def get_context_data(self, **kwargs):
        # Контекст шаблона
        context = super().get_context_data(**kwargs)
        # Добавляем список рубрик
        context['rubrics'] = Rubric.objects.all()
        return context


# Страница с рубрикой
def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'current_rubric': current_rubric
    }
    return render(request, 'bboard/by_rubric.html', context)


# Домашняя страница
def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {
        'bbs': bbs,
        'rubrics': rubrics
    }
    return render(request, 'bboard/index.html', context)
