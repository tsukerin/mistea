# В файле views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def save_changes(request):
    if request.method == 'POST':
        tea_type = request.POST.get('tea_type')
        schedule = request.POST.get('schedule')
        address = request.POST.get('address')

        # Обновление данных в базе данных
        user_profile = request.user.userprofile
        user_profile.user_subscription.tea_type = tea_type
        user_profile.user_subscription.schedule = schedule
        user_profile.user_subscription.address = address
        user_profile.user_subscription.save()

        return JsonResponse({'message': 'Изменения сохранены успешно.'})

    return JsonResponse({'message': 'Неверный запрос.'})

@login_required
def save_profile_changes(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        fullname = request.POST.get('fullname')
        phone_number = request.POST.get('phone_number')

        # Обновление данных в базе данных
        user = request.user
        user.email = email
        user.save()

        user_profile = user.userprofile
        user_profile.fullname = fullname
        user_profile.phone_number = phone_number
        user_profile.save()

        return JsonResponse({'message': 'Изменения сохранены успешно.'})

    return JsonResponse({'message': 'Неверный запрос.'})

