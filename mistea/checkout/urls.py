# payment/urls.py
from django.urls import path
from .views import *

app_name='checkout'

urlpatterns = [
    path('initial-payment/', initial_payment, name='initial_payment'),
    path('ukassa-webhook/', ukassa_webhook, name='ukassa_webhook'),
    path('get-payment-api/', get_payment_api, name='get_payment_api'),
    #path('payment/success/<str:personalized_identifier>/', yookassa_success, name='success'),
    path('success/<str:personalized_identifier>/', yookassa_success, name='success'),
]