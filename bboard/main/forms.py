# Формы
from captcha.fields import CaptchaField
from django import forms
from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage, Comment
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .apps import user_registered


# Правка данных пользователя
class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')


# Регистрация пользователя
class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Password (again)', widget=forms.PasswordInput,
                                help_text='Enter the same password again for verification')

    # Валидация пароля
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    # Совпадают ли пароли?
    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('The passwords entered do not match', code='password_mismatch')}
            raise ValidationError(errors)

    # Сохранения пользователя
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_messages')


# Форма подрубрики
class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(), empty_label=None, label='Super rubric',
                                          required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'


# Форма поиска
class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')


# Форма ввода объявления
class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


# Дополнительные иллюстрации
AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')


# Форма комментариев зарегистрированных пользователей
class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb': forms.HiddenInput}


# Форма комментариев гостей
class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Input text from image', error_messages={'invalid': 'False text'})

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb': forms.HiddenInput}
