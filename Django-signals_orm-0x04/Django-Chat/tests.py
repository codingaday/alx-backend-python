from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

# Task 1 Tests: Notification creation
class NotificationSignalTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pw')
        self.bob = User.objects.create_user(username='bob', password='pw')

    def test_notification_created_when_message_sent(self):
        msg = Message.objects.create(sender=self.alice, receiver=self.bob, content='Hi Bob!')
        notif = Notification.objects.filter(user=self.bob, message=msg).first()
        self.assertIsNotNone(notif)
        self.assertFalse(notif.is_read)

# Task 2 Tests: Message edit tracking
class MessageEditSignalTests(TestCase):
    def setUp(self):
        self.editor = User.objects.create_user(username='editor', password='pw')
        self.receiver = User.objects.create_user(username='receiver', password='pw')
        self.message = Message.objects.create(
            sender=self.editor,
            receiver=self.receiver,
            content='Original message'
        )

    def test_message_edit_creates_history(self):
        self.message.content = 'Edited message'
        self.message.edited_by = self.editor
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().previous_content, 'Original message')
        self.assertEqual(history.first().edited_by, self.editor)
        self.assertTrue(self.message.edited)
        self.assertIsNotNone(self.message.edited_at)

    def test_no_history_when_content_unchanged(self):
        self.message.content = 'Original message'
        self.message.edited_by = self.editor
        self.message.save()
        self.assertFalse(MessageHistory.objects.filter(message=self.message).exists())

# Task 3 Tests: Cleanup on user deletion
class UserDeletionSignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pw')
        self.other = User.objects.create_user(username='user2', password='pw')

        self.message = Message.objects.create(sender=self.user, receiver=self.other, content="Hi!")
        self.notification = Notification.objects.create(user=self.user, message=self.message)
        self.message.content = "Updated"
        self.message.edited_by = self.user
        self.message.save()  # triggers history

    def test_user_deletion_cleans_up_related_data(self):
        self.user.delete()
        self.assertFalse(Message.objects.filter(sender=self.user).exists())
        self.assertFalse(Notification.objects.filter(user=self.user).exists())
        self.assertFalse(MessageHistory.objects.filter(edited_by=self.user).exists())
