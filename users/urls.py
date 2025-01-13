from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from users import views

urlpatterns = [
    # Registration and Login
    path('register/', views.get_register, name='register'),  # Corrected to views.register
    path('login/', views.get_login, name='login'),            # Corrected to views.login
    path('home/', views.home, name='home'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh the access token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),    # Verify the access token
    path('profile/', views.get_profile, name='profile'),
    path('leaderboard/', views.get_leaderboard, name='leaderboard'),
]

