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
