from django.contrib import admin
from .models import ChatSession, Message

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['created_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender', 'timestamp']
    list_filter = ['sender', 'timestamp']
    search_fields = ['session__title', 'text', 'session__user__username']
    readonly_fields = ['timestamp']

