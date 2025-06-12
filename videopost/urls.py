# videopost/urls.py

from django.urls import path
from .views import reply_comment
from . import views
from .views import (
    VideoPostListView,
    VideoPostCreateView,
    VideoPostDetailView,
    VideoPostUpdateView,
    VideoPostDeleteView,
    VideoPostDetailViewId,
    VideoFeedView,
    archive_videopost,
    toggle_videolike,
    toggle_videodislike,
    search_video_results,
    videopost_api_detail,
    delete_videopost,
    # video_like,  # ✅ добавлен импорт
    # video_dislike, delete_videopost  # ✅ добавлен импорт
)

app_name = 'videopost'

urlpatterns = [

    path('', VideoPostListView.as_view(), name='videopost_list'),                       # 1. Главный список всех видеопостов
    path('create/', VideoPostCreateView.as_view(), name='videopost_create'),            # 2. Создание нового видеопоста
    path('feed/', VideoFeedView.as_view(), name='videopost_feed'),                      # 3. Лента подписок
    path('search/', search_video_results, name='search_video'),                         # 4. Поиск по видеопостам
    path('id/<int:pk>/', VideoPostDetailViewId.as_view(), name='videopost_detail_id'),  # 5. Детали по ID
    path('<slug:slug>/edit/', VideoPostUpdateView.as_view(), name='videopost_update'),  # 6. Редактирование
    path('<slug:slug>/delete/', VideoPostDeleteView.as_view(), name='videopost_delete'),# 7. Удаление
    path('<slug:slug>/archive/', archive_videopost, name='archive_videopost'),          # 8. Архивация
    path('<slug:slug>/like/', toggle_videolike, name='like_videopost'),                 # 9. Лайк через AJAX
    path('<slug:slug>/dislike/', toggle_videodislike, name='dislike_videopost'),        # 10. Дизлайк через AJAX
    path('api/<slug:slug>/', videopost_api_detail, name='videopost_api_detail'),        # 11. API-детали
    path('<slug:slug>/', VideoPostDetailView.as_view(), name='videopost_detail'),       # 12. Детали по slug (основной путь)
    path('video/<slug:slug>/', VideoPostDetailView.as_view(), name='video_detail'),     # 13. Альтернативный путь для детализации

    # 14. Лайк/дизлайк через POST-запросы (альтернативный путь)
    path('video/<slug:slug>/like/', toggle_videolike, name='video_like'),
    path('video/<slug:slug>/dislike/', toggle_videodislike, name='video_dislike'),

    path('<slug:slug>/ajax-delete/', delete_videopost, name='ajax_delete_videopost'),
    path('comment/<int:comment_id>/reply/', reply_comment, name='reply_comment'),

    path('share/', views.share_videopost, name='share_videopost'),

]
