from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .models import Bb, Rubric, Img

from .forms import BbForm, RubricBaseFormSet, SearchForm, ImgForm

from django.views.generic.detail import DetailView, SingleObjectMixin

from django.views.generic.list import ListView

from django.views.generic.dates import ArchiveIndexView

from django.views.generic.base import RedirectView

from django.core.paginator import Paginator

from django.forms import modelformset_factory, inlineformset_factory, formset_factory

from django.contrib.auth.views import redirect_to_login

from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

from django.db.transaction import atomic

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from sample_site.settings import BASE_DIR
from datetime import datetime
import os
from django.http import FileResponse

from django.http import JsonResponse
from .serializers import RubricSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


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
class BbAddView(SuccessMessageMixin, LoginRequiredMixin, FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}
    success_message = 'The advertisement for the sale of the product "%(title)s" has been created.'

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
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'page': page, 'bbs': page.object_list}
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


# Извлекает данные из SearchForm и использует их для указания параметров фильтрации объявлений
def search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            bbs = Bb.objects.filter(title__icontains=keyword, rubric=rubric_id)
            context = {'bbs': bbs}
            return render(request, 'bboard/search_results.html', context)
    else:
        sf = SearchForm()
    context = {'form': sf}
    return render(request, 'bboard/search.html', context)


# Обрабатка набор форм, не связанных с моделью
def formset_processing(request):
    FS = formset_factory(SearchForm, extra=3, can_order=True, can_delete=True)

    if request.method == 'POST':
        formset = FS(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    keyword = form.cleaned_data['keyword']
                    rubric_id = form.cleaned_data['rubric'].pk
                    order = form.cleaned_data['ORDER']
            return render(request, 'bboard/process_results.html')
    else:
        formset = FS(auto_id=False)
    context = {'formset': formset}
    return render(request, 'bboard/formset.html', context)


# Высокоуровневые средства для выгруженных файлов
# Сохранение выгруженного графического файла в модель
def add_image(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Image add', extra_tags='first second')
            form.save()
            return redirect('index')
    else:
        form = ImgForm()
        messages.warning(request, 'Warning please correct form!')

    context = {'form': form}
    return render(request, 'bboard/add_image.html', context)


# Удаление выгруженного графического файла с записью модели
def delete_image(request, pk):
    img = Img.objects.get(pk=pk)
    img.img.delete()
    img.delete()
    return redirect('index')

# Низкоуровневые средства для выгруженных файлов
# FILES_ROOT = os.path.join(BASE_DIR, 'media')


# Добавление
# def add_image(request):
#     if request.method == 'POST':
#         form = ImgForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = request.FILES['img']
#             fn = '%s%s' % (datetime.now().timestamp(), os.path.splitext(uploaded_file.name)[1])
#             fn = os.path.join(FILES_ROOT, fn)
#             with open(fn, 'wb+') as destination:
#                 for chunk in uploaded_file.chunks():
#                     destination.write(chunk)
#             # form.save()
#             return redirect('index')
#     else:
#         form = ImgForm()
#     context = {'form': form}
#     return render(request, 'bboard/add_image.html', context)


# Вывод
# def index_files(request):
#     imgs = []
#     for entry in os.scandir(FILES_ROOT):
#         imgs.append(os.path.basename(entry))
#     context = {'imgs': imgs}
#     return render(request, 'bboard/index_files.html', context)
#
#
# # Отправка файла клиенту
# def get(request, filename):
#     fn = os.path.join(FILES_ROOT, filename)
#     return FileResponse(open(fn, 'rb'), content_type='application/octet-stream')


# Вывод клиентам список рубрик в JSON (REST), Добавление рубрики
# Веб представление
@api_view(['GET', 'POST'])
def api_rubrics(request):
    if request.method == 'GET':
        rubrics = Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        return Response(serializer.data)
        # return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = RubricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Сведения об отдельной рубрике
# Изменение и удаление рубрики
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_rubric_detail(request, pk):
    rubric = Rubric.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = RubricSerializer(rubric)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = RubricSerializer(rubric, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        rubric.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Низкий уровень
# # Вывод рубрик и их добавление класс
# class APIRubrics(APIView):
#     def get(self, request):
#         rubrics = Rubric.objects.all()
#         serializer = RubricSerializer(rubrics, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = RubricSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # Правка, получение и удаление рубрики
# class APIRubricDetail(APIView):
#     def get(self, request, pk):
#         rubric = Rubric.objects.get(pk=pk)
#         serializer = RubricSerializer(rubric)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         rubric = Rubric.objects.get(pk=pk)
#         serializer = RubricSerializer(rubric, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         rubric = Rubric.objects.get(pk=pk)
#         rubric.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Высокий уровень
# Добавление и выдача рубрик
class APIRubrics(generics.ListCreateAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer


# Правка, удаление и получение рубрики
class APIRubricDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer


# Вывод рубрик
class APIRubricList(generics.ListAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer


# # Метаконтроллер класс, выполняющий все действия классов APIRubric и APIRubricDetail
# class APIRubricViewSet(ModelViewSet):
#     queryset = Rubric.objects.all()
#     serializer_class = RubricSerializer


# Метаконтроллер класс, только для чтения рубрик
class APIRubricViewSet(ReadOnlyModelViewSet):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
