from django.urls import path

from . import views

app_name = 'profile_app'

urlpatterns = [
    path('update/bio/', views.ProfileUpdateBIOView.as_view(), name='profile-bio-update'),
    path('update/password/', views.ProfileUpdatePasswordView.as_view(), name='profile-password-update'),
    path('update/avatar/', views.ProfileUpdateAvatarView.as_view(), name='profile-avatar-update'),
    path('users/', views.UsersListView.as_view(), name='users-profile'),
    path('<int:user_id>/', views.ProfileDetailView.as_view(), name='profile'),
]
