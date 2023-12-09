from django.urls import path

from main.views import TemplateAPIView

app_name = 'actions'

urlpatterns = [
    path('newsline/', TemplateAPIView.as_view(template_name='actions/newsline.html'), name='newsline'),
]
