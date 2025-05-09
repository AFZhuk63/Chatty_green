from django.urls import path
from . import views
from .views import PostUpdateView, PostDeleteView, PostCreateView, PostDetailView

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),                        # Список постов
    path('create/', PostCreateView.as_view(), name='post_create'),                   # Создание поста
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),           # Редактирование
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),       # Удаление
    path('<slug:slug>/like/', views.like_post, name='like_post'),                    # AJAX-лайк
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),              # Детали поста (в конце!)
]

