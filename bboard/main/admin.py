from django.contrib import admin
import datetime

from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage
from .utilities import send_activation_notification
from .forms import SubRubricForm


# Отправка писем с требованием активации
def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Requirement letters sent')


send_activation_notifications.short_description = 'Sending activation requests'


# Сортировка пользователей по активации
class NonactivatedFilter(admin.SimpleListFilter):
    title = 'You activated?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Gone'),
            ('threedays', 'More than 3 days have passed'),
            ('week', 'More than a week has passed'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


# Редактор пользователей
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'), ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'), 'groups', 'user_permissions', ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


# Редактор подрубрик встроенный
class SubRubricInline(admin.TabularInline):
    model = SubRubric


# Редактор надрубрик
class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)


# Редактор подрубрик
class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


# Редактор объявлений встроенный
class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


# Редактор объявлений
class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'price', 'contacts', 'image', 'is_active')
    inlines = (AdditionalImageInline,)


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
admin.site.register(Bb, BbAdmin)
