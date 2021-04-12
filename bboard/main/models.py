from django.db import models
from django.contrib.auth.models import AbstractUser


# Модель пользователя
class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Activated?')
    send_messages = models.BooleanField(default=True, verbose_name='Send notifications about new comments?')

    class Meta(AbstractUser.Meta):
        pass


# Рубрики (Базовая модель)
class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Name')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Order')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Subheading')


# Надрубрики
# Диспетчер записей
# Фильтр. Выбирает только записи с пустым полем super_rubric
class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


# Прокси модель, менять функциональность модели. Обработка только надрубрик
class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Super rubric'
        verbose_name_plural = 'Super rubrics'


# Подрубрики
# Фильтр только подрубрик
class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


# Прокси модель подрубрик
class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return f'{self.super_rubric.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Sub Rubric'
        verbose_name_plural = 'Sub Rubrics'
