from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class NotificationSignalTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pw')
        self.bob = User.objects.create_user(username='bob', password='pw')

    def test_notification_created_when_message_sent(self):
        msg = Message.objects.create(sender=self.alice, receiver=self.bob, content='Hi Bob!')
        notif = Notification.objects.filter(user=self.bob, message=msg).first()
        self.assertIsNotNone(notif)
        self.assertFalse(notif.is_read)
