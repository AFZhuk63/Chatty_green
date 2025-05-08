from django.urls import path
from . import views
from .views import PostUpdateView, PostDeleteView
from .views import PostCreateView

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),                       # Список постов
    path('create/', views.PostCreateView.as_view(), name='post_create'),                # Страница создания поста
    # path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail_by_id'),
    # path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),     # Страница детали поста
    path('<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),       # Страница редактирования поста
    path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),    # Страница удаления поста
]
