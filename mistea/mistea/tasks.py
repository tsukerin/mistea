import os
import django

from mistea.settings import ID_SHOP, SECRET_KEY

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mistea.settings")
django.setup()

from yookassa import Configuration, Payment
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from user.models import UserProfile
import time
from django.template.loader import render_to_string
from django.core.mail import send_mail

def send_message(user):
    user = user
    subject = 'Ваша подписка кончается!'
    html_message = render_to_string('checkout/email_send_end.html')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, '', from_email, recipient_list, html_message=html_message, fail_silently=False)

def add_subscription(user_id):
    user = User.objects.get(pk=user_id)
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    if not created:
        userprofile.subscription_end_date = timezone.now() + timedelta(days=30)
        userprofile.days_remaining = 30
        userprofile.save()


def decrease_subscription_days():
    for user in User.objects.all():
        userprofile, created = UserProfile.objects.get_or_create(user=user)
        userprofile.days_remaining -= 1
        userprofile.save()

        if userprofile.days_remaining == 3:
            send_message(user)
        elif userprofile.days_remaining == 0:
            userprofile.subscription = 0
            userprofile.save()
            Configuration.configure(ID_SHOP, SECRET_KEY)
            payment = Payment.create({
                "amount": {
                    "value": "2.00",
                    "currency": "RUB"
                },
                "capture": True,
                "payment_method_id": "<Идентификатор сохраненного способа оплаты>",
                "description": "Заказ №105"
            })

def main():
    decrease_subscription_days()

if __name__ == '__main__':
    main()