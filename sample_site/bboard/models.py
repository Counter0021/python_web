from django.db import models


# Модель объявлений
class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Product')
    content = models.TextField(null=True, blank=True, verbose_name='Description')
    price = models.FloatField(null=True, blank=True, verbose_name='Price')
    # db_index - создаст индекс, для сортировки по убыванию пригодится
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date')

    # Исправления
    class Meta:
        # Название во множественном числе
        verbose_name_plural = 'Advertisements'
        # Название в единственном числе
        verbose_name = 'Advertisement'
        # Сортировка полей
        ordering = ['-published']
