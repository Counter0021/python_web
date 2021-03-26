from django.forms import ModelForm

from .models import Bb


# Добавление новых объявления
class BbForm(ModelForm):
    # Параметры формы
    # model - класс, с которым она связана
    # fields - последовательность из имён модели, которые должны быть в форме
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
