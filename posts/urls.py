from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail_by_id'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
]