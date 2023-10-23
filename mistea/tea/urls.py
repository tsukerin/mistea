from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    # path('', home, name='home'),
    path('', index, name='index'),
    path('tea-list/', tea_list, name='tea-list'),
    path('about/', TemplateView.as_view(template_name='tea/about.html'), name='about'),
    path('subs/', subs, name='subs'),
    path('home/', subs, name='home'),
    path('tea-detail/<int:pk>/', tea_detail, name='tea-detail'), 
]