from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    # path('home/', home, name='home'),
    # path('', index, name='main'),
    path('', homepage, name='homepage'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    # path('about/', TemplateView.as_view(template_name='tea/about.html'), name='about'),
    path('subs/', subs, name='subs'),
    path('home/', subs, name='home'),
    path('tea-detail/<int:pk>/', tea_detail, name='tea-detail'),
    path('auth/', auth, name='auth'),
]