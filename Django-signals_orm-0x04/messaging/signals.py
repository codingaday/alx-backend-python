from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification, MessageHistory

# Signal for Task 1: Notify receiver on new message
@receiver(post_save, sender=Message)
def create_notification_for_receiver(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

# Signal for Task 2: Log message edits and previous content
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # This is a new message, not an edit

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            previous_content=old.content,
            edited_by=instance.edited_by  # should be set in the view
        )
        instance.edited = True
        instance.edited_at = timezone.now()
