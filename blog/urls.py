from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  
]