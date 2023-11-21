# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False)
    address = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'date_of_birth', 'address')

class LoginForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password2')