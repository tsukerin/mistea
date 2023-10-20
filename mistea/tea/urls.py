from django.urls import path
from .views import *

urlpatterns = [
    # path('', home, name='home'),
    path('', index, name='index'),
    path('tea-list/', tea_detail, name='tea-list'),
    path('tea-detail/<int:pk>/', tea_list, name='tea-detail'), 
]