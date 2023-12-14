# В файле urls.py

from django.urls import path
from .views import delete_profile, save_changes, save_profile_changes

urlpatterns = [
    path('save-changes/', save_changes, name='save_changes'),
    path('save-profile-changes/', save_profile_changes, name='save_profile_changes'),
    path('delete_profile/', delete_profile, name='delete_profile'),
]
