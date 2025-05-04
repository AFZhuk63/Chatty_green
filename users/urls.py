from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),  # главная страница
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),  # используем кастомное представление
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),  # Добавлен путь для редактирования профиля
]
