# payment/views.py
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from tea.models import Subscription
from user.models import UserProfile, UserSubscription
import uuid
import requests
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from mistea.tasks import check_subscription_status

def send_message(request, context):
    user = request.user
    subject = 'Подписка успешно оформлена'
    html_message = render_to_string('checkout/email_send.html', context)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, '', from_email, recipient_list, html_message=html_message, fail_silently=False)

@csrf_exempt
@login_required
def yookassa_success(request, personalized_identifier):
    user = request.user
    user_subscription = get_object_or_404(UserSubscription, personalized_identifier=personalized_identifier)
    usersubscription = user.userprofile.user_subscription
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.user_subscription = user_subscription
    user_profile.payment_date = datetime.now()
    user_profile.subscription = True
    user_profile.save()
    if not created:
        user_profile.subscription_end_date = datetime.now() + timedelta(days=30)
        user_profile.days_remaining = 30
        user_profile.save()

    subscription = user_subscription.sub_id
    context = {
        'subscription': subscription,
        'user_profile': user_profile, 
        'user_subscription': usersubscription, 
        'personalized_identifier': personalized_identifier
    }
    send_message(request, context)

    current_datetime = datetime.now()
    end_date = current_datetime + timedelta(days=30)
    check_subscription_status.apply_async(args=[user.id], eta=end_date)

    return render(request, 'checkout/success.html', {'user': user, 'user_profile': user_profile, 'personalized_identifier': personalized_identifier})

def already_have(request):
    return render(request, 'tea/error_window.html')
