from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory
from django.utils import timezone

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # new message, no edit
    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    if old.content != instance.content:
        # save history
        MessageHistory.objects.create(
            message=instance,
            previous_content=old.content
        )
        # mark edited
        instance.edited = True
        instance.edited_at = timezone.now()
