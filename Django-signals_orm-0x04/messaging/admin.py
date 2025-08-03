from django.contrib import admin
from .models import Message, MessageHistory

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'edited', 'edited_at', 'timestamp')
    readonly_fields = ('edited', 'edited_at')

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'updated_at')
    readonly_fields = ('previous_content', 'updated_at')
