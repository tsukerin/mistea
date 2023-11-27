# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.validators import RegexValidator

class RegForm(UserCreationForm):


    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email", )

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Пожалуйста, введите правильные имя пользователя и пароль. "
            "Оба поля могут быть чувствительны к регистру."
        ),
        'inactive': "Этот аккаунт неактивен.",
        'invalid_username': "Пожалуйста, введите корректное имя пользователя.",
        'invalid_password': "Пожалуйста, введите корректный пароль.",
        'custom_error': "Это ваше собственное сообщение об ошибке.",
    }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(required=False)
    address = forms.CharField(required=False, widget=forms.Textarea)
    phone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Введите корректный номер телефона.")],
        required=False,  # Разрешаем поле быть пустым
    )
    
    class Meta:
        model = UserProfile
        fields = ("date_of_birth", "address")
