from django.db import models
from django.contrib.auth.models import User

class Thread(models.Model):
    participants = models.ManyToManyField(User, verbose_name='Участники')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'

    def __str__(self):
        return f"Диалог {self.id}"
    
class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, verbose_name='Диалог')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель')
    text = models.TextField(max_length=5000, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Отправлено')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']

    def __str__(self):
        return f"Сообщение от {self.sender.username}"