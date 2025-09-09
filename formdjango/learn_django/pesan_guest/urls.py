from django.urls import path
from .views import contact_view, success_view

urlpatterns = [
    path('', contact_view, name='contact_view'),
    path('', success_view, name='success'),  # Tambahkan ini
]