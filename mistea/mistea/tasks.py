from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from tea.models import Subscription
from user.models import UserProfile
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import send_mail
from celery import shared_task
import logging

logger = logging.getLogger(__name__)
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@shared_task
def update_subscription_counter(user_id):
    try:
        user = User.objects.get(pk=user_id)
        profile = UserProfile.objects.get(user=user)

        if profile.days_remaining > 0:
            profile.days_remaining -= 1
            profile.save()
    except Exception as e:
        logger.error(f"Failed to update subscription counter: {e}")

@app.task
def check_subscription_status(user_id):
    user = User.objects.get(pk=user_id)
    profile = UserProfile.objects.get(user=user)
    subscription = get_object_or_404(Subscription, pk=profile.id)
    if profile.days_remaining <= 3:
        html_message = render_to_string('checkout/email_send_end.html', {'subscription': subscription})
    
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        subject = 'О нет!'
        send_mail(subject, '', from_email, recipient_list, html_message=html_message, fail_silently=False)
    else:
        update_subscription_counter.apply_async(args=[user.id], eta=profile.subscription_end_date)

