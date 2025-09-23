from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Thread, Message

@login_required
def messenger_home(request, thread_id=None):
    threads_list = []
    threads = Thread.objects.filter(participants=request.user).order_by('-updated_at')

    for thread in threads:
        thread_data = {
            'id': thread.id,
            'other_user': thread.participants.exclude(id=request.user.id).first(),
            'last_message': thread.message_set.last(),
            'unread_count': thread.message_set.filter(is_read=False).exclude(sender=request.user).count(),
            'updated_at': thread.updated_at,
            'is_active': thread.id == thread_id
        }
        threads_list.append(thread_data)
    
    active_thread = None
    active_messages = []
    other_user = None
    
    if thread_id:
        active_thread = get_object_or_404(Thread, id=thread_id, participants=request.user)
        other_user = active_thread.participants.exclude(id=request.user.id).first()
        active_messages = active_thread.message_set.all()
        Message.objects.filter(thread=active_thread).exclude(sender=request.user).update(is_read=True)
    
    context = {
        'threads_list': threads_list,
        'active_thread': active_thread,
        'active_messages': active_messages,
        'other_user': other_user,
        'title': 'Мессенджер'
    }
    return render(request, 'messenger/messenger_home.html', context)

@login_required
def start_thread(request, user_id):
    """Начать диалог с пользователем"""
    other_user = get_object_or_404(User, id=user_id)
    
    if request.user == other_user:
        return redirect('messenger:messenger_home')
    
    # Ищем существующий диалог
    thread = Thread.objects.filter(participants=request.user).filter(participants=other_user).first()
    
    if not thread:
        # Создаем новый диалог
        thread = Thread.objects.create()
        thread.participants.add(request.user, other_user)
    
    # Исправьте эту строку - используйте правильное имя URL
    return redirect('messenger:thread_detail', thread_id=thread.id)

@login_required
def users_list(request):
    """Список пользователей для нового диалога"""
    users = User.objects.exclude(id=request.user.id)
    
    context = {
        'users': users,
        'title': 'Выберите пользователя'
    }
    return render(request, 'messenger/users_list.html', context)

@login_required
def thread_detail(request, thread_id):
    """Страница чата с пользователем"""
    thread = get_object_or_404(Thread, id=thread_id, participants=request.user)
    
    # Получаем собеседника
    other_user = thread.participants.exclude(id=request.user.id).first()
    
    # Помечаем сообщения как прочитанные
    Message.objects.filter(thread=thread).exclude(sender=request.user).update(is_read=True)
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(
                thread=thread,
                sender=request.user,
                text=text
            )
            return redirect('messenger:thread_detail', thread_id=thread.id)
    
    messages = thread.message_set.all()
    
    context = {
        'thread': thread,
        'other_user': other_user,
        'messages': messages,
        'title': f'Чат с {other_user.username}'
    }
    return render(request, 'messenger/thread_detail.html', context)
