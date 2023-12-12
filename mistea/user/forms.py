from django import forms
from .models import UserSubscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserSubscription
        fields = ['schedule', 'tea_type' 'address']  # Укажите поля, которые вы хотите редактировать