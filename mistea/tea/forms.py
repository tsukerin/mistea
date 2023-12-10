# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Subscription
from user.models import UserProfile, UserSubscription
from django.core.validators import RegexValidator

class RegForm(UserCreationForm):


    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email", )

class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = self.fields.pop('email')

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['username'] = cleaned_data.get('email')
        return cleaned_data

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email", )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(required=True)
    class Meta:
        model = UserProfile
        fields = ('user_subscription',)

class UserSubscriptionForm(forms.ModelForm):
    address = forms.CharField(required=True, widget=forms.Textarea)
    phone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Введите корректный номер телефона.")],
        required=True,
    )
    message = forms.CharField(required=True)
    date_arrive = forms.DateField(
        input_formats=['%d.%m.%Y'],
    )
    tea_type = forms.ChoiceField(
        choices=[('1', 'Заварной'),
                ('2', 'В пакетиках')
                ],
                widget=forms.RadioSelect,
                required=True,
                initial='1',
                )
    schedule = forms.ChoiceField(
        choices=[
            ('1', 'Раз в месяц'),
            ('2', 'Раз в 2 месяца'),
            ('3', 'Раз в 3 месяца')
        ],
        widget=forms.RadioSelect,
        required=True,
        initial='1',
    )


    def clean(self):
        cleaned_data = super().clean()
        tea_type = cleaned_data.get('tea_type')
        schedule = cleaned_data.get('schedule')

        if tea_type == 'loose':
            cleaned_data['tea_type'] = 1
        elif tea_type == 'bagged':
            cleaned_data['tea_type'] = 2

        if schedule == 'monthly':
            cleaned_data['schedule_interval'] = 1
        elif schedule == 'every_two_months':
            cleaned_data['schedule_interval'] = 2
        elif schedule == 'every_three_months':
            cleaned_data['schedule_interval'] = 3

        return cleaned_data
            

    class Meta:
        model = UserSubscription
        fields = ('address', 'phone_number', 'message', 'date_arrive', 'schedule', 'tea_type')

        def __init__(self, *args, **kwargs):
            subscription_id = kwargs.pop('subscription_id', None)
            super().__init__(*args, **kwargs)

            if subscription_id:
                try:
                    subscription = Subscription.objects.get(pk=subscription_id)
                    self.fields['sub_id'].initial = subscription
                except Subscription.DoesNotExist:
                    pass


