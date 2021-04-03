from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .models import Bb, Rubric

from .forms import BbForm, RubricBaseFormSet

from django.views.generic.detail import DetailView, SingleObjectMixin

from django.views.generic.list import ListView

from django.views.generic.dates import ArchiveIndexView

from django.views.generic.base import RedirectView

from django.core.paginator import Paginator

from django.forms import modelformset_factory, inlineformset_factory

from django.contrib.auth.views import redirect_to_login

from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

from django.db.transaction import atomic


# Лучше избегать (взять контроллер более низкого лвла и реализовывать там всю логику самостоятельно)
# Смешанная функциональность (Вывод сведенья о выбранной записи и набор связанных с ней записей)
class BbByRubricView(SingleObjectMixin, ListView):
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg = 'rubric_id'

    # Извлекаем рубрику
    def get(self, request, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_rubric'] = self.object
        context['rubrics'] = Rubric.objects.all()
        context['bbs'] = context['object_list']
        return context

    # Возвращаем перечень объявлений, связанных с найденной рубрикой
    def get_queryset(self):
        return self.object.bb_set.all()


# Перенаправление
class BbRedirectView(RedirectView):
    url = '/bboard/detail/%(pk)d/'


# Хронологический список записей
class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# Удаление
class BbDeleteView(PermissionRequiredMixin, DeleteView):
    # Разрешаем удалять только тем, кто имеет право 'bboard.delete_bb'
    permission_required = ('bboard.delete_bb',)
    model = Bb
    success_url = '/bboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# Исправление объявления
class BbEditView(UserPassesTestMixin, UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/bboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    # Разрешаем исправлять объявления только пользователям со статусом суперюзер
    def test_func(self):
        return self.request.user.is_superuser


# Лучше использовать CreateView
# Добавление нового объявления
# Доступ к добавлению только зарегистрированных пользователей
class BbAddView(LoginRequiredMixin, FormView):
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


# # Вывод объявлений из рубрики
# class BbByRubricView(ListView):
#     template_name = 'bboard/by_rubric.html'
#     context_object_name = 'bbs'
#
#     def get_queryset(self):
#         return Bb.objects.filter(rubric=self.kwargs['rubric_id'])
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
#         return context


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


# Домашняя страница с пагинатором
def index(request):
    # Выполнил ли юзер вход?
    # if request.user.is_authenticated:
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubrics': rubrics, 'page': page, 'bbs': page.object_list}
    return render(request, 'bboard/index.html', context)


# Наборы форм
# Допускает к странице только пользователей, выполнивших вход
@login_required
# Допуск только тех, кто имеет права
@permission_required(('bboard.add_rubric', 'bboard.change_rubric', 'bboard.delete_rubric'))
def rubrics(request):
    # Непосредственные проверки авторизации
    if request.user.is_authenticated:
        RubricFormSet = modelformset_factory(Rubric, fields=('name',), can_delete=True, formset=RubricBaseFormSet)
        if request.method == 'POST':
            formset = RubricFormSet(request.POST)
            if formset.is_valid():
                formset.save()
                return redirect('index')
        else:
            formset = RubricFormSet()
        context = {'formset': formset}
        return render(request, 'bboard/rubrics.html', context)
    else:
        return redirect_to_login(reverse('index'))


# Автоматическое выполнение транзакций
# Либо для объединения транзакции использовать декоратор
# @atomic
# Встроенные наборы форм
def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.method == 'POST':
        formset = BbsFormSet(request.POST, instance=rubric)
        if formset.is_valid():
            # Выполняем сохранение всех форм в 1 транзакции
            with atomic():
                formset.save()
            return redirect('index')
    else:
        formset = BbsFormSet(instance=rubric)
    context = {'formset': formset, 'current_rubric': rubric}
    return render(request, 'bboard/bbs.html', context)
