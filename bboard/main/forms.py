# Формы
from django import forms
from .models import AdvUser


# Правка данных пользователя
class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')
