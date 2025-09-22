from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm
from django.db.models import Q
from django.core.paginator import Paginator

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
                post.status = 'published'
                message = 'Пост успешно опубликован!'
            else:
                post.status = 'pending'
                message = 'Пост успешно создан и отправлен на модерацию!'
            
            post.save()
            messages.success(request, message)
            return redirect('home')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'title': 'Создание нового поста'
    }
    return render(request, 'blog/create_post.html', context)
        
@login_required
@login_required
def edit_post(request, post_id):
    # Получаем пост из базы данных
    post = get_object_or_404(Post, id=post_id)
    
    # Проверяем права доступа
    if post.author != request.user:
        messages.error(request, 'Вы не можете редактировать этот пост!')
        return redirect('blog:post_detail', post_id=post.id)  # ← ИМЯ МАРШРУТА, а не шаблона
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.author = request.user
            updated_post.save()
            messages.success(request, 'Пост успешно обновлен!')
            return redirect('blog:post_detail', post_id=post.id)  # ← ИМЯ МАРШРУТА
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, 'Вы не можете удалить этот пост!')
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост успешно удален!')
        return redirect('home')
    
    return render(request, 'blog/delete_post.html', {'post': post})

def post_list(request):
    posts = Post.objects.filter(status='published').select_related('author', 'category').order_by('-created_at')
    
    search_query = request.GET.get('q') 
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'posts': page_posts,
        'categories': categories,
    }

    return render(request, 'blog/post_list.html', context)