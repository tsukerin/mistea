from django.urls import path
from .views import *
from django.conf.urls import include

urlpatterns = [
    path('home/', homepage, name='home'),
    path('', homepage, name='homepage'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    # path('about/', TemplateView.as_view(template_name='tea/about.html'), name='about'),
    path('subs/', subs, name='subs'),
    path('subscribe/', subscribe, name='subscribe'),
    path('tea-detail/<int:pk>/', tea_detail, name='tea-detail'),
    path('profile/', ProfileView.as_view(), name='profile'), 
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('auth/', include('django.contrib.auth.urls')),
    path('subscription/<int:subscription_id>/', subscription_detail, name='subscription_detail'),
    path('subscr/<int:subscription_id>/', subscr, name='subscr'),

]