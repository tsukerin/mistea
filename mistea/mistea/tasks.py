# tasks.py
import dramatiq
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from dramatiq.brokers.redis import RedisBroker
from user.models import UserProfile


dramatiq.set_broker(RedisBroker())
@dramatiq.actor
def process_subscription(user_id):
    user = User.objects.get(pk=user_id)
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    if not created:
        userprofile.subscription_end_date = timezone.now() + timedelta(days=30)
        userprofile.days_remaining = 30
        userprofile.save()

    decrease_subscription_days.send_with_options(args=[user_id,], delay=timedelta(seconds=1))

@dramatiq.actor
def decrease_subscription_days(user_id):
    user = User.objects.get(pk=user_id)
    userprofile = UserProfile.objects.get_or_create(user=user)
    userprofile.days_remaining -= 1
    userprofile.save()

    if userprofile.days_remaining == 3:
        send_mail(
            'Предупреждение о завершении подписки',
            'Ваша подписка закончится через 3 дня. Пожалуйста, продлите ее.',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
