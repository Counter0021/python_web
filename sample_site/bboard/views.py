from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.urls import reverse_lazy, reverse

from .models import Bb, Rubric

from .forms import BbForm

from django.views.generic.detail import DetailView

from django.views.generic.list import ListView


# Исправление объявления
class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/bboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# Добавление нового объявления
class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    # Контекст шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    # Валидация формы, сохранение её
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # Получить форму, чтобы перенаправить потом на страницу с данной катигорией
    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    # Перенаправить на url категорий
    def get_success_url(self):
        return reverse('by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


# Вывод объявлений из рубрики
class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context


# Вывод страницы с объявлением, выбранным посетителем
class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# # Контроллер класс, для обработки формы
# class BbCreateView(CreateView):
#     # Путь к файлу шаблона, создающего страницу с формой
#     template_name = 'bboard/create.html'
#     # Ссылка на класс формы, связанной с моделью
#     form_class = BbForm
#     # Интернет-адрес для перенаправления после успешного сохранения данных
#     success_url = reverse_lazy('index')
#
#     # Вывод перечня рубрик, он формирует контекст шаблона
#     def get_context_data(self, **kwargs):
#         # Контекст шаблона
#         context = super().get_context_data(**kwargs)
#         # Добавляем список рубрик
#         context['rubrics'] = Rubric.objects.all()
#         return context


# # Страница с рубрикой
# def by_rubric(request, rubric_id):
#     bbs = Bb.objects.filter(rubric=rubric_id)
#     rubrics = Rubric.objects.all()
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {
#         'bbs': bbs,
#         'rubrics': rubrics,
#         'current_rubric': current_rubric
#     }
#     return render(request, 'bboard/by_rubric.html', context)


# Домашняя страница
def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {
        'bbs': bbs,
        'rubrics': rubrics
    }
    return render(request, 'bboard/index.html', context)
