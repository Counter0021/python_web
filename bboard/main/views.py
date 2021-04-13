from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import AdvUser, SubRubric, Bb
from .forms import ChangeUserInfoForm, RegisterUserForm, SearchForm, BbForm, AIFormSet
from .utilities import signer


# Home page
# Вывод последних 10 объявлений
def index(request):
    bbs = Bb.objects.filter(is_active=True)[:10]
    context = {'bbs': bbs}
    return render(request, 'main/index.html', context)


# Вывод вспомогательных страниц в 1 контроллере
def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


# Логин пользователя
class BBLoginView(LoginView):
    template_name = 'main/login.html'


# Профиль пользователя, его объявления
@login_required
def profile(request):
    bbs = Bb.objects.filter(author=request.user.pk)
    context = {'bbs': bbs}
    return render(request, 'main/profile.html', context)


# Выход пользователя
class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


# Правка данных пользователя
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'User data updated'

    # Извлекаем ключ пользователя
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    # Извлечение исправляемой записи
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# Смена пароля
class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Password user updated'


# Регистрация пользователя
class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


# Сообщения об успешной регистрации
class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


# Активация пользователя
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


# Удаление пользователя
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    # Получаем ключ пользователя
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    # Выход пользователя и сообщение об удалении
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User deleted')
        return super().post(request, *args, **kwargs)

    # Извлечение исправляемой записи
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# Сбросс пароля. Отправка письма для сброса пароля
class PasswordResetUserView(PasswordResetView):
    template_name = 'main/reset_password.html'
    subject_template_name = 'email/reset_subject.txt'
    email_template_name = 'email/reset_email.txt'
    success_url = reverse_lazy('main:password_reset_done')


# Уведомление об отправке письма для сброса пароля
class PasswordResetDoneUserView(PasswordResetDoneView):
    template_name = 'main/reset_password_done.html'


# Сбросс пароля
class PasswordResetConfirmUserView(PasswordResetConfirmView):
    template_name = 'main/confirm_password.html'
    success_url = reverse_lazy('main:password_reset_complete')


# Уведомление об успешном сброссе пароля
class PasswordResetCompleteUserView(PasswordResetCompleteView):
    template_name = 'main/complete_password.html'


# Рубрики
# Страница выбранной рубрики
def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=rubric)
    # Фильтрация по слову
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''

    form = SearchForm(initial={'keyword': keyword})
    # Пагинатор с 2 записями
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'bbs': page.object_list, 'form': form}
    return render(request, 'main/by_rubric.html', context)


# Страница выбранного объявления
def detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'main/detail.html', context)


# Объявления пользователя
@login_required
def profile_bb_detail(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'main/profile_bb_detail.html', context)


# Добавление объявлений
@login_required
def profile_bb_add(request):
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Add advertisement')
                return redirect('main:profile')

    else:
        form = BbForm(initial={'author': request.user.pk})
        formset = AIFormSet()

    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_bb_add.html', context)
