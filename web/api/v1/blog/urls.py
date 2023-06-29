from django.urls import path

from api.v1.blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article-list'),
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('create/', views.ArticleCreateView.as_view(), name='article-create'),
    path('tag/', views.TagListView.as_view(), name='tag-list'),
    path('comments/<slug:article_slug>', views.CommentListView.as_view(), name='comment-list'),
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
]
