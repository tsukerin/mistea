# В файле urls.py

from django.urls import path
from .views import save_changes

urlpatterns = [
    # Добавьте URL-маршрут
    path('save-changes/', save_changes, name='save_changes'),
    # ...
]
