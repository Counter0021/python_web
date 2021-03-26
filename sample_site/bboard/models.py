from django.db import models


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
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Rubric')

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
