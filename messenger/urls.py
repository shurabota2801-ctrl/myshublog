from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.messenger_home, name='messenger_home'),
    path('thread/<int:thread_id>/', views.messenger_home, name='messenger_home_thread'),
    path('detail/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('start/<int:user_id>/', views.start_thread, name='start_thread'),
    path('users/', views.users_list, name='users_list'),
]