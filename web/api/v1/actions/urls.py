from django.urls import path

from . import views

app_name = 'actions'

urlpatterns = [
    path('', views.VotesView.as_view(), name='like-dislike'),
    path('walls/', views.EventView.as_view(), name='walls'),
    path('followers/update/', views.FollowerUpdateDeleteView.as_view(), name='followers-update'),
    path('following/', views.FollowerViewSet.as_view({'get': 'following_current_user'}), name='following-current-user'),
    path('followers/', views.FollowerViewSet.as_view({'get': 'followers_current_user'}), name='followers-current-user'),
    path('following/<int:user_id>/', views.FollowerViewSet.as_view({'get': 'following_by_id'}), name='following-by-id'),
    path('followers/<int:user_id>/', views.FollowerViewSet.as_view({'get': 'followers_by_id'}), name='followers-by-id'),
]
