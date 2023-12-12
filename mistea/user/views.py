# В файле views.py

from django.shortcuts import render
from django.http import JsonResponse

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
