# payment/views.py
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from tea.models import Subscription
from user.models import UserProfile, UserSubscription
import uuid
import requests
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings

authorization = "Mjg2OTM3OnRlc3RfcE5wZTNCcDczS3YzRFRyQkF0a29YdFpVTmZIUFBGdWFtV1RacDlvNDRWQQ=="
initial_payment_msg = "Списываем оплату за заказ"
my_url = "https://www.instagram.com/sprestay/"

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            response_data = {
                "status": "error",
                "body": str(e)
            }
            return render(args[0], 'checkout/error_template.html', {'response_data': response_data}, status=500)

    return wrapper

@csrf_exempt
@handle_exception
def initial_payment(request):
    url = "https://api.yookassa.ru/v3/payments"
    order_id = request.POST.get("order_id")
    try:
        order = Order.objects.get(order_id=order_id)
        price = order.price
        headers = {
            "Authorization": authorization,
            "Idempotence-Key": str(uuid.uuid4()),
            "Content-Type": 'application/json'
        }
        params = {
            "amount": {
                "value": "100",
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": request.build_absolute_uri(reverse('payment:payment-success'))
            },
            "description": initial_payment_msg,
            "save_payment_method": "false"
        }

        
        response_data = requests.post(url, json=params, headers=headers).json()
        if response_data["status"] == "pending":
            order.payment_id = response_data["payment_method"]["id"]
            order.save()
            response_data["order_id"] = order.order_id
    except Order.DoesNotExist:
        response_data = {"order_id": order_id}

    return render(request, 'checkout/initial_payment_template.html', {'response_data': response_data})

@csrf_exempt
@handle_exception
def ukassa_webhook(request):
    if request.POST.get("event") == "payment.waiting_for_capture":
        payment_id = request.POST.get("object.id")
        status = request.POST.get("object.status")
        if status == "waiting_for_capture":
            confirm_payment(payment_id)
            get_payment(payment_id)
    return HttpResponse("OK")

def confirm_payment(payment_id):
    order = Order.objects.get(payment_id=payment_id)
    order.paid = True
    order.save()
    print('Документ успешно обновлен')

def get_payment(payment_id):
    url = f"https://api.yookassa.ru/v3/payments/{payment_id}/capture"
    headers = {
        "Authorization": authorization,
        "Idempotence-Key": str(uuid.uuid4()),
        "Content-Type": 'application/json'
    }
    response_data = requests.post(url, headers=headers).json()
    print("Платеж успешно подтвержден", response_data)
    return True

def cancel_payment(payment_id):
    url = f"https://api.yookassa.ru/v3/payments/{payment_id}/cancel"
    headers = {
        "Authorization": authorization,
        "Idempotence-Key": str(uuid.uuid4()),
        "Content-Type": 'application/json'
    }
    response_data = requests.post(url, headers=headers).json()
    print("Платеж успешно отменен", response_data)
    return True

@csrf_exempt
@handle_exception
def get_payment_api(request):
    payment_id = request.POST.get("payment_id")
    get_payment(payment_id)
    return HttpResponse(status=200)

@csrf_exempt
@handle_exception
def cancel_payment_api(request):
    payment_id = request.POST.get("payment_id")
    cancel_payment(payment_id)
    return HttpResponse(status=200)

@csrf_exempt
@login_required
def yookassa_success(request, personalized_identifier):
    user = request.user
    user_subscription = user.userprofile.user_subscription
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.user_subscription = user_subscription
    user_profile.payment_date = timezone.now()
    user_profile.subscription = True
    user_profile.save()
    subscription = get_object_or_404(Subscription, pk=user_profile.id)
    subject = 'Подписка успешно оформлена'
    
    # Отрендерим HTML-шаблон как строку
    html_message = render_to_string('checkout/email_send.html', {'subscription': subscription, 'user_profile': user_profile, 'user_subscription': user_subscription, 'personalized_identifier': personalized_identifier})
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Используем send_mail с параметром html_message для отправки HTML-контента
    send_mail(subject, '', from_email, recipient_list, html_message=html_message, fail_silently=False)

    return render(request, 'checkout/success.html', {'user': user, 'user_profile': user_profile, 'personalized_identifier': personalized_identifier})

