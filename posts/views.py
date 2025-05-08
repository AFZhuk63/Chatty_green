from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import CreateView
from .forms import PostForm


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_list')  # или на detail по slug, на выбор

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})


# def post_detail_by_slag(request, slug): # исправить slag → slug (если это ошибка и создан не намеренно):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'posts/post_detail.html', {'post': post})


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['text', 'image']
    template_name = 'posts/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'posts/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        # Получаем объект Post по slug
        return Post.objects.get(slug=self.kwargs['slug'])