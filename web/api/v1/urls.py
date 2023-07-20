from django.urls import include, path, re_path

app_name = 'v1'

urlpatterns = [
    path('auth/', include('api.v1.auth_app.urls')),
    path('article/', include('api.v1.blog.urls')),
    path('contact/', include('api.v1.contact_us.urls')),
    path('profile/', include('api.v1.profile_app.urls')),
    re_path('actions/', include('api.v1.actions.urls')),
]
