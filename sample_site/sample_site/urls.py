from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.staticfiles.views import serve
from django.views.static import serve as media_serve

from django.views.decorators.cache import never_cache

urlpatterns = [
    path('bboard/', include('bboard.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='registration/change_password.html'),
         name='password_change'),
    path('accounts/password_change/done/',
         PasswordChangeDoneView.as_view(template_name='registration/password_changed.html'),
         name='password_change_done'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='registration/reset_password.html',
                                                               subject_template_name='registration/reset_subject.txt',
                                                               email_template_name='registration/reset_email.txt'),
         name='password_reset'),
    path('accounts/password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name='registration/email_sent.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='registration/confirm_password.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/',
         PasswordResetCompleteView.as_view(template_name='registration/password_confirmed.html'),
         name='password_reset_complete'),
    path('captcha/', include('captcha.urls')),
    path('social/', include('social_django.urls', namespace='social')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Отключить кэширование статических файлов на стороне клиента
# if settings.DEBUG:
#     urlpatterns.append(path('static/<path:path>', never_cache(serve)))

# Публикация сайта. Обработка статических файлов
if not settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', serve, {'insecure': True}))
    urlpatterns.append(path('media/<path:path>', media_serve, {'document_root': settings.MEDIA_ROOT}))
