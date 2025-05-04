from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import CustomUser  # если переопределялась модель
from .forms import CustomUserCreationForm, CustomPasswordChangeForm  # если форма расширялась
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomUserEditForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', username=user.username)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'users/profile.html', {'user': user})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Редиректим на страницу профиля пользователя
            return redirect('profile', username=user.username)
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


class CustomLoginView(LoginView):
    def get_success_url(self):
        return f'/profile/{self.request.user.username}'


def edit_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=user)  # Используйте нужную форму
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = CustomUserCreationForm(instance=user)  # Предзаполненная форма

    return render(request, 'users/edit_profile.html', {'form': form, 'user': user})


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Необходимо для сохранения авторизации после смены пароля
            messages.success(request, 'Пароль был успешно изменен!')
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # Твой шаблон входа

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})