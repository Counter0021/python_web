from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Модель объявлений
class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Product')
    content = models.TextField(null=True, blank=True, verbose_name='Description')
    price = models.FloatField(null=True, blank=True, verbose_name='Price')
    # db_index - создаст индекс, для сортировки по убыванию пригодится
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date')
    # Поле внешнего ключа, устанавливающее связь между текущей записью этой модели и записью модели Rubric
    # (связь один-со-многими)
    # on_delete=models.PROTECT чтобы после удаления категории, объявления остались
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.CASCADE, verbose_name='Rubric')

    # Исправления
    class Meta:
        # Название во множественном числе
        verbose_name_plural = 'Advertisements'
        # Название в единственном числе
        verbose_name = 'Advertisement'
        # Сортировка полей
        ordering = ['-published']


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Name')

    class Meta:
        verbose_name_plural = 'Rubrics'
        verbose_name = 'Rubric'
        ordering = ['name']

    def __str__(self):
        return self.name


# Полиморфная связь
# Заметки для связи с моделями
class Note(models.Model):
    content = models.TextField()
    # Поле, хранящее тип связываемой модели
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # Поле, хранящее ключ связываемой записи
    object_id = models.PositiveIntegerField()
    # Поле полиморфной связи
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')


# Абстрактная модель
class Message(models.Model):
    content = models.TextField()
    name = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        abstract = True
        ordering = ['name']


class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Переопределяем поле
    name = models.CharField(max_length=40)
    # Удаляем поле
    email = None

    # Наследуем класс Meta
    class Meta(Message.Meta):
        pass


# Прокси модель
# Сортировка рубрик по названию
class RevRubric(Rubric):
    class Meta:
        proxy = True
        ordering = ['-name']
