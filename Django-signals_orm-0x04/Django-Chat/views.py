from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def send_message(request, receiver_id):
    if request.method == 'POST':
        receiver = get_object_or_404(User, id=receiver_id)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')  # For threaded replies
        parent_message = Message.objects.filter(id=parent_id).first() if parent_id else None

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )
    return render(request, 'messaging/message_sent.html')


@login_required
def conversation_view(request, user_id):
    # Fetch top-level messages
    messages = Message.objects.filter(
        sender=request.user,
        receiver_id=user_id,
        parent_message__isnull=True
    ).select_related('receiver', 'sender').prefetch_related('replies')

    # Recursive thread fetch
    def get_all_replies(message):
        replies = list(message.replies.select_related('sender', 'receiver').all())
        for reply in replies:
            reply.child_replies = get_all_replies(reply)
        return replies

    threaded_messages = []
    for msg in messages:
        msg.child_replies = get_all_replies(msg)
        threaded_messages.append(msg)

    return render(request, 'messaging/conversation.html', {'threaded_messages': threaded_messages})


@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return render(request, 'messaging/account_deleted.html')
    return render(request, 'messaging/confirm_delete.html')
