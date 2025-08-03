from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_thread_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_thread_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return f'{self.sender} to {self.receiver}'

    def get_thread(self):
        return self.replies.select_related('sender', 'receiver').prefetch_related('replies').all()
