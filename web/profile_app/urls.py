from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views import TemplateAPIView

app_name = 'profile_app'

urlpatterns = [
    path('users/', TemplateAPIView.as_view(template_name='profile_app/users.html'), name='profile-users'),
    path('profile/', TemplateAPIView.as_view(template_name='profile_app/profile.html'), name='profile'),
    path('profile/<int:user_id>', TemplateAPIView.as_view(template_name='profile_app/unauthorized_profile.html'), name='unauthorized-profile')
]
