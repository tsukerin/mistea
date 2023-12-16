from django.urls import path
from .views import *
from django.conf.urls import include

urlpatterns = [
    path('', homepage, name='homepage'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('profile/', ProfileView.as_view(), name='profile'), 
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('auth/', include('django.contrib.auth.urls')),
    path('subscription/<int:subscription_id>/', subscription_detail, name='subscription_detail'),
    path('order/<int:subscription_id>/', OrderSub.as_view(), name='order'),
    path('profile/delete_subscription/', DeleteSubscriptionView.as_view(), name='delete_subscription'),
]