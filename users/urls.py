from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', extra_context={'title': 'Вход в систему'}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', extra_context={'title': 'Выход из системы'}), name='logout'),
]

