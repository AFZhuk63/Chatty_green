# subscriptions/views.py

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Count, Exists, OuterRef
from posts.models import Post
from .models import Subscription
from pprint import pprint

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class SubscriptionToggleView(LoginRequiredMixin, View):
    """
    Представление для подписки/отписки от пользователя.
    Поддерживает AJAX и обычные запросы.
    """

    def post(self, request, username):
        print("\n--- HEADERS ---")
        pprint(dict(request.headers))
        print("--- COOKIES ---")
        pprint(request.COOKIES)
        # Получаем автора, на которого подписываемся или от которого отписываемся
        author = get_object_or_404(User, username=username)

        # Проверяем, не пытается ли пользователь подписаться на самого себя
        if request.user == author:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Вы не можете подписаться на самого себя'
                }, status=400)
            else:
                # Для обычного запроса перенаправляем обратно на профиль
                return redirect('profile', username=username)

        # Проверяем, подписан ли уже пользователь
        subscription = Subscription.objects.filter(
            subscriber=request.user,
            author=author
        ).first()

        if subscription:
            # Если подписка существует, удаляем её (отписываемся)
            subscription.delete()
            is_subscribed = False
            message = f'Вы отписались от {author.username}'
        else:
            # Если подписки нет, создаём её (подписываемся)
            try:
                Subscription.objects.create(subscriber=request.user, author=author)
                is_subscribed = True
                message = f'Вы подписались на {author.username}'
            except IntegrityError:
                # Обработка редкого случая одновременного создания подписки
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Подписка уже существует'
                    }, status=400)
                else:
                    return redirect('profile', username=username)

        # Получаем URL для перенаправления после завершения операции
        next_url = request.POST.get('next')

        # Возвращаем ответ в зависимости от типа запроса (AJAX или обычный)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Формируем JSON-ответ для AJAX-запроса
            return JsonResponse({
                'subscribed': is_subscribed,  # 🔧 ключ должен быть именно таким!
                'message': message,
                'subscribers_count': author.followers.count(),
            })

        else:
            # Для обычного запроса перенаправляем  на профиль
            if next_url:
                return redirect(next_url)
            else:
                return redirect('profile', username=username)


class FollowersListView(ListView):
    """
    Отображает список подписчиков пользователя.
    """
    model = Subscription
    template_name = 'subscriptions/followers.html'
    context_object_name = 'subscriptions'
    paginate_by = 10

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, username=self.kwargs['username'])
        return Subscription.objects.filter(author=self.profile_user).exclude(
            subscriber=self.profile_user).select_related('subscriber')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.profile_user

        # Если пользователь авторизован, определяем, на кого из списка он подписан
        if self.request.user.is_authenticated:
            subscribed_to = set(
                Subscription.objects.filter(
                    subscriber=self.request.user,
                    author__in=[sub.subscriber for sub in context['subscriptions']]
                ).values_list('author_id', flat=True)
            )
            context['subscribed_to'] = subscribed_to

        return context


class FollowingListView(ListView):
    """
    Отображает список подписок пользователя (на кого он подписан).
    """
    model = Subscription
    template_name = 'subscriptions/following.html'
    context_object_name = 'subscriptions'
    paginate_by = 10

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, username=self.kwargs['username'])
        # Получаем подписки, где profile_user является подписчиком
        return Subscription.objects.filter(subscriber=self.profile_user).select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.profile_user
        return context


class FeedView(LoginRequiredMixin, ListView):
    """
    Отображает ленту постов от пользователей, на которых подписан текущий пользователь.
    """
    model = Post
    template_name = 'subscriptions/feed.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Post.objects.none()

        # Получаем ID пользователей, на которых подписан текущий пользователь
        following_users = Subscription.objects.filter(
            subscriber=self.request.user
        ).values_list('author_id', flat=True)

        # Возвращаем посты от этих пользователей с аннотациями для количества лайков и комментариев
        return Post.objects.filter(
            author_id__in=following_users
        ).select_related('author').annotate(
            num_comments=Count('comments', distinct=True),
            num_likes=Count('likes', distinct=True)
        ).order_by('-publication_date')


@login_required
def toggle_subscription(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return JsonResponse({'error': 'Нельзя подписаться на самого себя'}, status=400)

    subscription, created = Subscription.objects.get_or_create(
        subscriber=request.user,
        author=target_user
    )

    if not created:
        subscription.delete()
        is_subscribed = False
    else:
        is_subscribed = True

    subscribers_count = Subscription.objects.filter(author=target_user).count()

    return JsonResponse({
        'is_subscribed': is_subscribed,
        'subscribers_count': subscribers_count,
    })