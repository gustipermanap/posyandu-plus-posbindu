"""
URLs untuk auth-service.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('user-info/', views.user_info, name='user-info'),
    path('update-profile-picture/', views.update_profile_picture, name='update-profile-picture'),
]
