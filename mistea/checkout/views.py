# payment/views.py
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from tasks.views import add_subscription, send_message
from tea.models import Subscription
from user.models import UserProfile, UserSubscription
import uuid
import requests
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings

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

    subscription = user_subscription.sub_id
    context = {
        'subscription': subscription,
        'user_profile': user_profile, 
        'user_subscription': user_subscription, 
        'personalized_identifier': personalized_identifier
    }
    send_message(request, context)
    add_subscription(user.id, user_subscription.schedule)

    return render(request, 'checkout/success.html', {'user': user, 'user_profile': user_profile, 'personalized_identifier': personalized_identifier})

def already_have(request):
    return render(request, 'tea/error_window.html')
