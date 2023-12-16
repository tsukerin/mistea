from django.contrib import admin
from django.urls import path, include
from tasks.views import decrease_subscription_days
from tea.views import *


urlpatterns = [
    path('update_subscribes/', decrease_subscription_days, name='decrease_subscription_days')
]
