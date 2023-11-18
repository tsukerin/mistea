# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "E-mail",
                "class": "u-custom-font u-heading-font u-input u-input-rectangle u-radius-25 u-input-2"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "u-custom-font u-heading-font u-input u-input-rectangle u-radius-25 u-input-2"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "u-custom-font u-heading-font u-input u-input-rectangle u-radius-25 u-input-2"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "u-custom-font u-heading-font u-input u-input-rectangle u-radius-25 u-input-2"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "u-custom-font u-heading-font u-input u-input-rectangle u-radius-25 u-input-2"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "u-custom-font u-heading-font u-input u-input-rectangle u-radius-25 u-input-2"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
