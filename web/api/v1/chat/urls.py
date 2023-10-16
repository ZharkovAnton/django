from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('userinfo/', views.UserChatListView.as_view(), name='chat-userinfo'),
]
