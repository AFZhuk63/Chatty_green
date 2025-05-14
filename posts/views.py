#posts/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from posts.templatetags import time_filters
from posts.models import Post


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context['posts']:
            post.likes_count = post.likes.count()
            post.dislikes_count = post.dislikes.count()
            post.likes_users = post.likes.all()
            post.dislikes_users = post.dislikes.all()
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    #fields = ['text', 'image']
    template_name = 'posts/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'slug': self.object.slug})  # ✅ Добавляем namespace


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
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
            return redirect('post_list')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


@login_required
@require_POST
def like_post(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to like a post.")

    post = get_object_or_404(Post, slug=slug)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })

@require_POST
def dislike_post(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to dislike a post.")

    post = get_object_or_404(Post, slug=slug)
    user = request.user

    if user in post.dislikes.all():
        post.dislikes.remove(user)
        disliked = False
    else:
        post.dislikes.add(user)
        disliked = True
        post.likes.remove(user)  # ❗ убираем лайк, если ставится дизлайк

    return JsonResponse({
        'disliked': disliked,
        'dislikes_count': post.dislikes.count()
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
    print(f'pk_url_kwarg = {pk_url_kwarg}')


def archive_post(request, slug):
    if request.method == "POST":
        post = get_object_or_404(Post, slug=slug)
        if request.user == post.author:
            post.is_archived = True  # Должно быть поле `is_archived`
            post.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def home(request):
    latest_posts = Post.objects.filter(is_archived=False).order_by('-created_at')[:5]  # 5 свежих постов
    print(f"🔍 Передача в шаблон: {latest_posts}")  # Проверяем консоль
    return render(request, 'home.html', {'latest_posts': latest_posts})
