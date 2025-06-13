#posts/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from .models import Post, Comment, Advertisement
from .forms import CommentForm, PostForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from subscriptions.models import Subscription
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from posts.templatetags import time_filters
from django.db.models import Q


# Классы для работы с Post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(is_archived=False).order_by('-created_at')  # ✅ Самые свежие посты сверху

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context["paginator"]
        page = self.request.GET.get("page")

        try:
            page = int(page) if page else 1  # ✅ Преобразуем `page` в `int`
            if page > paginator.num_pages:  # ✅ Если запрашиваемая страница больше доступных
                context["invalid_page"] = True  # ⚠ Передаём флаг ошибки в шаблон
                context["last_page"] = paginator.num_pages  # ✅ Передаём последнюю доступную страницу
        except (ValueError, PageNotAnInteger, EmptyPage):
            context["invalid_page"] = True
            context["last_page"] = 1  # ✅ Если ошибка, перенаправляем на первую страницу

        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'slug': self.object.slug})  # ✅ Добавляем namespace


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:post_list')
    template_name = 'posts/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Детали поста с формой комментариев (CBV)
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all() # Подключаем комментарии
        context['form'] = CommentForm() # Форма для новых комментариев
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('posts:post_list') # после добавления комментария пользователь перенаправляется на список постов, а не остаётся на том же посте.
            # return redirect('posts:post_detail', slug=self.object.slug) # после добавления комментария пользователь остается на этой же странице

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


@login_required
@require_POST
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        if post.dislikes.filter(id=user.id).exists():
            post.dislikes.remove(user)
        post.likes.add(user)
        liked = True

    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes_count': post.likes.count(),
        'dislikes_count': post.dislikes.count(),  # Добавлено для синхронизации
    })

@login_required
@require_POST
def dislike_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    if post.dislikes.filter(id=user.id).exists():
        post.dislikes.remove(user)
        disliked = False
    else:
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
        post.dislikes.add(user)
        disliked = True

    return JsonResponse({
        'success': True,
        'disliked': disliked,
        'likes_count': post.likes.count(),  # Добавлено для синхронизации
        'dislikes_count': post.dislikes.count(),
    })

class PostDetailViewSlug(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'  # Поле модели для поиска по слагу
    slug_url_kwarg = 'slug'  # Название параметра в URL


class PostDetailViewId(DetailView):
    model = Post
    template_name = 'post_detail.html'  # Можно использовать тот же шаблон
    context_object_name = 'post'
    pk_field = 'pk'
    pk_url_kwarg = 'pk'  # Явное указание параметра URL



class FeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    paginate_by = 10 # Количество постов на одной странице

    def get_queryset(self):
        # Получаем список авторов, на которых подписан текущий пользователь
        subscribed_authors = Subscription.objects.filter(subscriber=self.request.user).values_list('author', flat=True)
        # Фильтруем посты только от этих авторов
        # return Post.objects.filter(author__in=subscribed_authors).order_by('-publication_date') # ленивая загрузка
        # return Post.objects.filter(author__in=subscribed_authors).select_related("author").order_by('-publication_date') # ленивая загрузка
        # return Post.objects.filter(author__in=subscribed_authors).select_related("author").prefetch_related("tags").order_by('-publication_date') # Если у постов есть ManyToMany или обратные связи (например, comments) используем ускоренную загрузку,
        return Post.objects.filter(author__in=subscribed_authors).select_related("author").prefetch_related("tags").order_by('-publication_date')  # Жадная загрузка # Если у постов есть ManyToMany или обратные связи (например, comments) используем ускоренную загрузку,


def archive_post(request, slug):
    if request.method == "POST":
        post = get_object_or_404(Post, slug=slug)
        if request.user == post.author:
            post.is_archived = True  # Должно быть поле `is_archived`
            post.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def home(request):
    # Выбираем 5 последних неархивированных постов, отсортированных по дате создания (от новых к старым)
    latest_posts = Post.objects.filter(is_archived=False).order_by('-created_at')[:12]
    return render(request, 'home.html', {'latest_posts':  latest_posts})


def delete_post(request, slug):
    if request.method == "POST":
        post = get_object_or_404(Post, slug=slug)
        if request.user == post.author:
            post.is_archived = True
            post.save()
            return JsonResponse({"success": True, "post_id": post.id, "message": "✅ Ваш пост успешно удалён!"})

    return JsonResponse({"success": False, "error": "❌ Ошибка удаления поста"})


def search_results(request):
    query = request.GET.get("q", "").strip()
    posts = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query), is_archived=False)

    return render(request, "posts/search_results.html", {"posts": posts, "query": query})




