from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views import TemplateAPIView

app_name = 'profile_app'

urlpatterns = [
    path('profile/', TemplateAPIView.as_view(template_name='profile_app/profile.html'), name='profile'),
    path('users/', TemplateAPIView.as_view(template_name='profile_app/users.html'), name='profile-users'),
]
