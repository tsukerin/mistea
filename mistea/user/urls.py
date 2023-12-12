# В файле urls.py

from django.urls import path
from .views import save_changes, save_profile_changes

urlpatterns = [
    # Добавьте URL-маршрут
    path('save-changes/', save_changes, name='save_changes'),
     path('save-profile-changes/', save_profile_changes, name='save_profile_changes'),

    # ...
]
