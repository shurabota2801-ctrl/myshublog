from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm

def index(request):
    latest_posts = Post.objects.filter(
        status='published'
    ).select_related('author', 'category').order_by('-created_at')[:6]
    
    context = {
        'posts': latest_posts,
        'title': 'Главная страница ShuBlog'
    }
    return render(request, 'index.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    post.views += 1
    post.save(update_fields=['views'])
    context = {'post': post, 'title': post.title}
    return render(request, 'blog/post_detail.html', context)

def post_list(request):
    posts = Post.objects.filter(status='published').select_related('author', 'category') 
    context = {
        'posts': posts,
        'title': 'Все посты'
    }
    return render(request, 'blog/post_list.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if request.user.is_staff or request.user.is_superuser:
                post.status = 'Published'
                message = 'Пост успешно опубликован!'
            else:
                post.status = 'pending'
                message = 'Пост успешно создан и отправлен на модерацию!'
            
            post.save()
            messages.success(request, message)
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'title': 'Создание нового поста'
    }
    return render(request, 'blog/create_post.html', context)