from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory

User = get_user_model()

class MessageEditLoggingTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pw')
        self.bob = User.objects.create_user(username='bob', password='pw')
        self.msg = Message.objects.create(sender=self.alice, receiver=self.bob, content='Hello')

    def test_history_created_on_edit(self):
        self.msg.content = 'Hi Bob!'
        self.msg.save()

        self.msg.refresh_from_db()
        history = MessageHistory.objects.filter(message=self.msg)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().previous_content, 'Hello')
        self.assertTrue(self.msg.edited)
        self.assertIsNotNone(self.msg.edited_at)

    def test_no_history_when_content_same(self):
        self.msg.content = 'Hello'
        self.msg.save()
        self.assertFalse(MessageHistory.objects.filter(message=self.msg).exists())
