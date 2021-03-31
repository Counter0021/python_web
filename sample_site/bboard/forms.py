from django.forms import ModelForm, modelform_factory, DecimalField, BaseModelFormSet
from django import forms

from .models import Bb, Rubric

from django.forms.widgets import Select

from django.core import validators
from django.core.validators import ValidationError


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
    title = forms.CharField(label='Name product', validators=[validators.RegexValidator(regex='^.{4,}$')],
                            error_messages={'invalid': 'Product with a very short name'})
    price = forms.DecimalField(label='Price', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Rubric', help_text='Please choose rubric!',
                                    widget=forms.widgets.Select(attrs={'size': 8}))

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Name product'}

    # Валидация определённого поля
    def clean_title(self):
        val = self.cleaned_data['title']
        if val == 'Last year snow':
            raise ValidationError('Not allowed for sale')
        return val

    # Валидация формы
    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Please enter a product description')

        if self.cleaned_data['price'] < 0:
            errors['price'] = ValidationError('Enter a non-negative price value')

        if errors:
            raise ValidationError(errors)


# Валидация наборов форм
class RubricBaseFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        names = [form.cleaned_data['name'] for form in self.forms if 'name' in form.cleaned_data]
        if 'Property' not in names:
            raise ValidationError('Add rubric property!')

