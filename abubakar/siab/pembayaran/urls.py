from django.urls import path
from . import views

urlpatterns = [
    path('tagihan/', views.lihat_tagihan, name='lihat_tagihan'),
]
