from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin

from users import views

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # User-related pages
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),  # User registration page (HTML)
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),  # Login page (HTML)
    
    # User-related API
    path('api/users/', include('users.urls')),  # API for /api/users/ endpoints

    # Game-related pages and API
    path('game/', TemplateView.as_view(template_name='playgame.html'), name='playgame'),
  # Game pages (HTML)
    path('api/game/', include('game.urls')),  # API for /api/game/ endpoints

    # Home page
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]
