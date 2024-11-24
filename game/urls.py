# game/urls.py
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('play/', views.start_game, name='play_game'),
    path('get_opponents/', views.show_opponents, name='get_opponents'),
    path('submit_score/<int:game_id>/', views.submit_score, name='submit_score'),
    path('game_history/', views.game_history, name='get_game_history'),
]
