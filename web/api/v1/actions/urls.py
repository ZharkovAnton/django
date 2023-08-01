from django.urls import path

from . import views

app_name = 'actions'

urlpatterns = [
    path('', views.VotesView.as_view(), name='like-dislike'),
    path('followers/update/', views.FollowerUpdateDeleteView.as_view(), name='followers-update'),
    path('following/<int:user_id>/', views.FollowerViewSet.as_view({'get': 'following'}), name='user-following'),
    path('followers/<int:user_id>/', views.FollowerViewSet.as_view({'get': 'followers'}), name='user-followers'),
]
