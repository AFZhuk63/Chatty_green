<<<<<<< HEAD
[S1] Создать GitHub-репозиторий chatty. Настроить базовую структуру: chatty/, users/, templates/, .gitignore, README.md.

Acceptance Criteria:

# Репозиторий создан.
Django-проект и базовая структура каталогов добавлены.
.gitignore исключает временные и служебные файлы.
README.md содержит название проекта и инструкции по запуску.

# 1. Создание корневой директории
mkdir Chatty_green
cd Chatty_green

# 2. Создание виртуального окружения
python -m venv venv

# 3. Активация виртуального окружения
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Установка Django
pip install django

# 5. Создание проекта с названием chatty
django-admin startproject chatty .

# 6. Проверка запуска сервера
python manage.py runserver
# открываем в браузере http://127.0.0.1:8000 и видим приветственную страницу Django.
```
The install worked successfully! Congratulations!
View release notes for Django 5.2
You are seeing this page because DEBUG=True is in your settings file and you have not configured any URLs.
Django"...
```
# Chatty_green
```
Обновленная и упрощенная схема проекта
Chatty_green/
├── chatty/                          # Django-проект
│   ├── __init__.py
│   ├── settings.py                  # Настройки (будет разделение на base/dev/prod)
│   ├── urls.py                      # Корневой роутинг
│   ├── asgi.py
│   └── wsgi.py
│
├── core/                            # Общие компоненты
│   ├── templates/                   # Базовые шаблоны (base.html, 404.html и др.)
│   ├── static/                      # Общие CSS, JS, изображения
│   ├── utils.py                     # Вспомогательные функции
│   └── views.py                     # Статические страницы (о проекте, ошибки)
│
├── users/                           # Пользователи
│   ├── models.py                    # Модель профиля
│   ├── forms.py                     # Регистрация, логин, редактирование
│   ├── views.py                     # Регистрация, логин, профиль
│   ├── urls.py
│   ├── templates/users/             # Шаблоны профиля, формы и т.д.
│   └── admin.py
│
├── posts/                           # Посты и комментарии
│   ├── models.py                    # Post, Comment, Like
│   ├── forms.py                     # Форма создания поста, комментария
│   ├── views.py                     # CRUD-представления
│   ├── urls.py
│   ├── templates/posts/            # Шаблоны для постов и ленты
│   └── admin.py
│
├── subscriptions/                  # Подписки
│   ├── models.py                    # Subscription
│   ├── views.py                     # Подписка/отписка
│   ├── urls.py
│   └── templates/subscriptions/    # Шаблоны подписок
│
├── templates/                      # Глобальные шаблоны (если не в app)
│   └── base.html
│
├── manage.py
├── venv/
├── requirements.txt                # Зависимости
├── .env                            # Переменные окружения
└── docker/                         # Docker конфигурации
    ├── Dockerfile
    ├── docker-compose.yml
    └── nginx/
        └── default.conf
```
# Связи между приложениями:

users.UserProfile связан с posts.Post и subscriptions.Subscription
posts.Post связан с users, subscriptions, posts.Comment, posts.Like
subscriptions.Subscription — связь "пользователь → подписки"

# Команды:
```
В корне проекта Chatty_green (где находится manage.py) выполняем:

python manage.py startapp users
python manage.py startapp posts
python manage.py startapp subscriptions
python manage.py startapp core
```
# Открываем chatty/settings.py и добавяем в INSTALLED_APPS:

```
INSTALLED_APPS = [
    # Системные
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Наши приложения которые мы добавили 
    'users',
    'posts',
    'subscriptions',
    'core',
]
```

======= 
# Структура проекта (по уровням)

1. Корневая папка проекта Chatty_green/
```
Содержит:
venv/ — виртуальное окружение Python
manage.py — точка входа в Django
requirements.txt — список зависимостей
.env — переменные окружения (секреты, БД, отладка)
docker/ — контейнеризация (Dockerfile, nginx, gunicorn)
chatty/ — Django-конфигурация проекта
```
2. Папка проекта chatty/
```
Содержит:
settings.py — конфигурация проекта (будет разбита на base, dev, prod)
urls.py — глобальные маршруты
wsgi.py, asgi.py — интерфейсы для запуска сервера
__init__.py — инициализация Python-пакета
```
3. Приложение users/ — Пользователи
```
Назначение:
Регистрация, вход, выход, редактирование профиля
Хранение пользовательских данных (аватар, биография)
Расширение модели пользователя (OneToOne)

Содержит:
models.py — UserProfile (OneToOne с User)
forms.py — формы регистрации, входа, редактирования
views.py — логика отображения и обработки профиля
urls.py — маршруты пользователей
templates/users/ — шаблоны регистрации, входа, профиля
admin.py — настройка отображения профилей в админке
```
4. Приложение posts/ — Публикации
```
Назначение:
CRUD-посты с изображениями
Комментарии и лайки

Содержит:
models.py: Post, Comment, Like
forms.py: форма создания поста, комментария
views.py: отображение ленты, деталки, добавление/редактирование постов
urls.py: маршруты постов и комментариев
templates/posts/: шаблоны ленты, комментариев, публикаций
admin.py: управление постами в админке
```
5. Приложение subscriptions/ — Подписки
```
Назначение:
Система подписок между пользователями
Возможность следить за постами подписанных людей

Содержит:
models.py: Subscription (ManyToMany через модель)
views.py: подписка/отписка, список подписчиков
urls.py
templates/subscriptions/: шаблоны отображения подписок
admin.py: отображение подписок в админке
```
6. Приложение core/ — Общие компоненты
```
Назначение:
Базовые шаблоны, общие утилиты, обработка ошибок, страницы "О проекте", 404/500 и т.д.

Содержит:
views.py: страницы вроде "О нас", 404/500
utils.py: вспомогательные функции (например, сокращение текста, генерация имени файла)
templates/core/: base.html, 404.html, 500.html, about.html
static/: общие CSS/JS (например, Bootstrap, кастомные стили)
```
7. Связи между моделями
```
User ←→ UserProfile (1 к 1)
UserProfile ←→ Post (1 ко многим)
Post ←→ Comment, Like (1 ко многим)
User ←→ Subscription ←→ User (модель подписки через ManyToMany)
Post.image — изображение с обработкой загрузки
```
8. Навигация/маршруты (urls)
```
/ — Главная лента постов
/users/register/, /users/login/, /users/logout/, /users/<username>/ — вход, выход, регистрация, профиль
/posts/create/, /posts/<id>/edit/, /posts/<id>/delete/ — управление постами
/posts/<id>/ — детальный просмотр поста
/subscriptions/, /subscribe/<id>/ — управление подписками
/about/ — информация о проекте
/admin/ — панель администратора
```
9. Технологический стек
```
Backend: Django 4+
Frontend: HTML, Bootstrap (возможно Tailwind)
БД: SQLite на dev, PostgreSQL на prod
Auth: Стандартная + расширение профиля
DevOps: Docker, docker-compose, Nginx, Gunicorn
Media: Django media storage для аватарок и изображений постов
```
# ЭТАПЫ РЕАЛИЗАЦИИ ПРОЕКТА
# Шаг 1: Модель пользователя и профиля (users/models.py)
```
Создаем базовую модель users/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import os

def avatar_upload_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    avatar = models.ImageField(upload_to=avatar_upload_path, default='avatars/default.jpg', verbose_name='Аватар')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Уменьшаем размер аватара при сохранении
        if self.avatar:
            img_path = self.avatar.path
            img = Image.open(img_path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(img_path)
```
# Шаг 2. Связь моделей — в apps.py и сигналах
Создадим сигнал, чтобы при создании User автоматически создавался UserProfile.
# users/signals.py
```
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```
# Шаг 3. Подключим сигнал в apps.py
```
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals

```
# Шаг 3. Миграции
```
python manage.py makemigrations users
python manage.py migrate
```
# Шаг 4: Регистрация профиля в админке 
# users/admin.py
```
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
```

# Шаг 5. Базовую навигацию urls.py и шаблоны. Структура URL-ов

Cоздадаем:
```
Главный маршрут (chatty/urls.py)
Подключение приложения users
Базовый шаблон с навигацией (layout)
# Шаг 2. Связь моделей — в apps.py и сигналах
```
# 5.1. Основной файл маршрутов Chatty/urls.py
```
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # маршруты пользователей
]

# Подключение медиафайлов (аватары)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
# 5.1. users/urls.py — маршруты внутри приложения users
# users/urls.py
```
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
]
```
# 6. Подключение шаблонов
Структура папок шаблонов:
```
chatty_green/
│
├── templates/
│   ├── users/
│   │   ├── login.html
│   │   ├── logout.html
│   │   ├── register.html
│   │   └── profile.html
│   └── base.html
```
Шаблон templates/base.html (OlgaFaruk)
```
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Chatty{% endblock %}</title>

    <!-- Подключение Bootstrap через CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <!-- Дополнительные стили -->
    <style>
        body {
            font-family: Arial, sans-serif;
            padding-top: 56px; /* Добавьте если используете fixed navbar */
        }
    </style>
</head>
<body>
    <!-- Включение навигационной панели (ТОЛЬКО ЗДЕСЬ) -->
    {% include "include/navbar.html" %}

    <main class="container mt-4">
        {% block content %}
        <!-- Здесь будет контент страниц -->
        {% endblock %}
    </main>

    <!-- Включение футера -->
    {% include "include/footer.html" %}
</body>
</html>


# users/urls.py
```
templates/users/register.html
```
{% extends "base.html" %}
{% block content %}
<h2>Регистрация</h2>
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Зарегистрироваться</button>
</form>
{% endblock %}
```
Финальные настройки в settings.py

 settings.py
```
... другие настройки ...

#Authentication settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'your_app.CustomUser'  # <-- вот здесь

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # для collectstatic
STATICFILES_DIRS = [BASE_DIR / 'static']  # дополнительные папки со статикой

 ... остальные настройки ...
 
 P.S. заменили ALLOWED_HOSTS = [] на ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'web']  # 'web' - имя сервиса в docker-compose
```
# Обновления для signals.py
Улучшенная версия:
```
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile

User = settings.AUTH_USER_MODEL  # Используем кастомную модель пользователя

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Создает или обновляет профиль пользователя при сохранении модели User.
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        # Безопасное обновление без рекурсии
        if hasattr(instance, 'profile'):
            instance.profile.save()
```
# Доработан apps.py
```
Добавлена строка в class UsersConfig(AppConfig):
default_auto_field = 'django.db.models.BigAutoField'
```
# Эта реализация:

- Использует кастомную модель пользователя
- Избегает рекурсии
- Обрабатывает случаи, когда профиль уже существует
- Более безопасна и соответствует современным стандартам Django


