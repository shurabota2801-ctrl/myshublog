from django.shortcuts import render
from blog.models import Post

def index(request):
    latest_posts = Post.objects.filter(
        status='published'
    ).select_related('author', 'category').order_by('-created_at')[:6]
    
    context = {
        'posts': latest_posts,
        'title': 'Главная страница ShuBlog'
    }
    return render(request, 'index.html', context)
