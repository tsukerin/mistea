# payment/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
import uuid
import requests

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

def success(request):
    return render(request, 'checkout/success.html')