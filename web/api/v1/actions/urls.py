from django.urls import path

from . import views

app_name = 'actions'

urlpatterns = [
    path('', views.VotesView.as_view(), name='like-dislike'),
]
