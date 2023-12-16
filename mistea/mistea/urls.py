from django.contrib import admin
from django.urls import path, include
from tea.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tea.urls')),
    path('payment/', include('checkout.urls')),
    path('user/', include('user.urls')),
]
