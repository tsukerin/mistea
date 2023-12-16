# payment/urls.py
from django.urls import path
from .views import *

app_name='checkout'

urlpatterns = [
    path('success/<str:personalized_identifier>/', yookassa_success, name='success'),
    path('already_have/', already_have, name='already')
]