from django.forms import ModelForm, modelform_factory, DecimalField
from django import forms

from .models import Bb, Rubric

from django.forms.widgets import Select


# Если редко используется
# # Фабрика классов modelform_factory()
# BbForm = modelform_factory(Bb,
#                            fields=('title', 'content', 'price', 'rubric'),
#                            labels={'title': 'Name product'},
#                            help_texts={'rubric': 'Please choose rubric!'},
#                            field_classes={'price': DecimalField},
#                            widgets={'rubric': Select(attrs={'size': 8})})


# # Добавление новых объявления
# class BbForm(ModelForm):
#     # Параметры формы
#     # model - класс, с которым она связана
#     # fields - последовательность из имён модели, которые должны быть в форме
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')


# # Полное объявление формы
# class BbForm(ModelForm):
#     title = forms.CharField(label='Name product')
#     content = forms.CharField(label='Description product',
#                               widget=forms.widgets.Textarea())
#     price = forms.DecimalField(label='Price', decimal_places=2)
#     rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
#                                     label='Rubric', help_text='Please choose rubric!',
#                                     widget=forms.widgets.Select(attrs={'size': 8}))
#
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')


# Полное объявление отдельных полей формы
class BbForm(ModelForm):
    price = forms.DecimalField(label='Price', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Rubric', help_text='Please choose rubric!',
                                    widget=forms.widgets.Select(attrs={'size': 8}))

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Name product'}
