# в файле forms.py
from django import forms

class CreateOrderForm(forms.Form):
    price = forms.DecimalField()
    # Добавьте другие поля заказа по необходимости
