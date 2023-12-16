from django.http import HttpResponse
from django.shortcuts import render
from yookassa import Configuration, Payment
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from user.models import UserProfile
import time
from django.template.loader import render_to_string
from django.core.mail import send_mail
import requests
# Create your views here.

def send_message(user):
    user = user
    subject = 'Ваша подписка кончается!'
    html_message = render_to_string('checkout/email_send_end.html')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, '', from_email, recipient_list, html_message=html_message, fail_silently=False)

def add_subscription(user_id, schedule):
    user = User.objects.get(pk=user_id)
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    if not created:
        userprofile.subscription_end_date = timezone.now() + timedelta(days=30)
        if schedule == 1:
            userprofile.days_remaining = 30
        elif schedule == 2:
            userprofile.days_remaining = 60
        elif schedule == 3:
            userprofile.days_remaining = 90
        userprofile.save()

def decrease_subscription_days(request):
    for user in User.objects.all():
        userprofile, created = UserProfile.objects.get_or_create(user=user)
        if userprofile.days_remaining != False:
            userprofile.days_remaining -= 1
            userprofile.save()
    
            if userprofile.days_remaining == 3:
                send_message(user)
            elif userprofile.days_remaining == 1:
                if userprofile.user_subscription.schedule == 1:
                    userprofile.days_remaining = 30
                elif userprofile.user_subscription.schedule == 2:
                    userprofile.days_remaining = 60
                elif userprofile.user_subscription.schedule == 3:
                    userprofile.days_remaining = 90
                userprofile.save()
                Configuration.configure('286937', 'test_pNpe3Bp73Kv3DTrBAtkoXtZUNfHPPFuamWTZp9o44VA')
                payment = Payment.create({
                    "amount": {
                        "value": userprofile.user_subscription.price,
                        "currency": "RUB"
                    },
                    "capture": True,
                    "payment_method_id": "<>",
                    "description": "Авто-оплата"
                })
            elif userprofile.days_remaining == 0:
                userprofile.subscription = 0
                userprofile.save()
    return HttpResponse(200)
