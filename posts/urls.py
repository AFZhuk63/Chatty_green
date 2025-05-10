from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailViewSlug.as_view(), name='post_detail_slug'),
    path('id/<int:pk>/', views.PostDetailViewId.as_view(), name='post_detail_id'),
#    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
]