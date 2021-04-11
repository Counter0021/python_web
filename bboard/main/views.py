from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Home page
def index(request):
    return render(request, 'main/index.html')


# Вывод вспомогательных страниц в 1 контроллере
def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


# Логин
class BBLoginView(LoginView):
    template_name = 'main/login.html'


# Профиль
@login_required
def profile(request):
    return render(request, 'main/profile.html')


# Выход
class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'
