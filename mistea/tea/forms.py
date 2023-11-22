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
        fields = UserCreationForm.Meta.fields + ("email", )

class LoginForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password2')