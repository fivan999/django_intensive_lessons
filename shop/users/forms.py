import django.forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm
)

import users.models


class BootstrapForm(django.forms.ModelForm):
    """для красивого отображения других форм"""

    def __init__(self, *args, **kwargs) -> None:
        """переорпеделяем поля"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class SignUpForm(BootstrapForm, UserCreationForm):
    """форма регистрации"""

    class Meta(UserCreationForm.Meta):
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
        model = users.models.ShopUser

    def __init__(self, *args, **kwargs) -> None:
        """переопределяем поля"""
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields[
            'username'
        ].help_text = 'Не более 150 символов. '
        'Только буквы, цифры и символы @/./+/-/_.'

        self.fields['email'].label = 'Почта'
        self.fields['email'].help_text = 'Введите адрес электронной почты'

        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].help_text = 'Придумайте пароль'

        self.fields['password2'].label = 'Пароль еще раз'
        self.fields['password2'].help_text = 'Подтвердите пароль'


class CustomAuthenticationForm(AuthenticationForm):
    """форма авторизации"""

    def __init__(self, *args, **kwargs) -> None:
        """переопределяем поля"""
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].help_text = 'Введите имя польвователя'

        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Введите пароль'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CustomPasswordChangeForm(PasswordChangeForm):
    """форма смены пароля"""

    def __init__(self, *args, **kwargs) -> None:
        """переопределяем поля"""
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Старый пароль'
        self.fields['old_password'].help_text = 'Введите старый пароль'

        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password1'].help_text = 'Придумайте пароль'

        self.fields['new_password2'].label = 'Пароль еще раз'
        self.fields['new_password2'].help_text = 'Подтвердите пароль'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CustomPasswordResetForm(PasswordResetForm):
    """форма для отправки письма для восстановления пароля"""

    def __init__(self, *args, **kwargs) -> None:
        """переопределяем поля"""
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Почта'
        self.fields[
            'email'
        ].help_text = 'Введите электронную почту, к которой привязан аккаунт'
        self.fields['email'].widget.attrs['class'] = 'form-control'


class CustomSetPasswordForm(SetPasswordForm):
    """форма для нового пароля"""

    def __init__(self, *args, **kwargs) -> None:
        """переопределяем поля"""
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password1'].help_text = 'Придумайте пароль'

        self.fields['new_password2'].label = 'Пароль еще раз'
        self.fields['new_password2'].help_text = 'Подтвердите пароль'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CustomUserChangeForm(BootstrapForm, UserChangeForm):
    """форма изменения пользователя"""

    password = None

    class Meta:
        model = users.models.ShopUser
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        help_texts = {
            'username': 'Введите имя пользователя',
            'email': 'Введите электронную почту',
            'first_name': 'Ввеите имя',
            'last_name': 'Введите фамилию'
        }


class ProfileChangeForm(BootstrapForm):
    """форма изменения профиля"""

    class Meta:
        model = users.models.Profile
        fields = ('birthday', 'image')
        labels = {
            'birthday': 'Дата рождения',
            'image': 'Аватарка'
        }
        help_texts = {
            'birthday': 'Введите дату рождения в формате день.месяц.год',
            'image': 'Загрузите аватарку'
        }
