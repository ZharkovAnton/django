from django.urls import path
from django.views.generic import TemplateView

from main.views import TemplateAPIView

app_name = 'auth_app'


urlpatterns = [
    path('login/', TemplateAPIView.as_view(template_name='auth_app/login.html'), name='login'),
    path('register/', TemplateAPIView.as_view(template_name='auth_app/sign_up.html'), name='sign_up'),
    path(
        'password-recovery/',
        TemplateAPIView.as_view(template_name='auth_app/reset_password_email.html'),
        name='reset_email_sent',
    ),
    path(
        'password-change/', TemplateView.as_view(template_name='auth_app/password_change.html'), name='password_change'
    ),
    path(
        'verify-email/', TemplateView.as_view(template_name='auth_app/verify_email.html'), name='account_verification'
    ),
]
