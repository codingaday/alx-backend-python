

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Custom User Manager (Optional but good practice for custom users)
# This manager allows for creating users and superusers with the custom fields.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin') # Set default role for superuser

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# User Model
class User(AbstractUser):
    # Override the default primary key with a UUID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Fields from schema, some are already in AbstractUser (first_name, last_name, email)
    # email is already unique in AbstractUser, but we explicitly ensure it's indexed.
    email = models.EmailField(unique=True, null=False, db_index=True) # Explicitly indexed as per schema

    # password_hash is handled by Django's AbstractUser.set_password()

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # Role as an ENUM, using choices in Django
    class Role(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST,
        null=False
    )

    # created_at is handled by Django's AbstractUser.date_joined,
    # but we can add an explicit one if needed for consistency with schema.
    # For now, let's rely on date_joined from AbstractUser for 'created_at' equivalent.
    # If a separate 'created_at' is strictly required, uncomment and add:
    # created_at = models.DateTimeField(default=timezone.now, editable=False)

    # Remove username field as email will be used for authentication
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role'] # Fields required when creating a user

    objects = CustomUserManager() # Assign the custom manager

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# Conversation Model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Many-to-Many relationship with User for participants
    # 'User' refers to the custom User model defined above
    participants = models.ManyToManyField(User, related_name='conversations')
    
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        # Optional: Add an index on created_at if frequently queried by time
        # indexes = [
        #     models.Index(fields=['created_at']),
        # ]


# Message Model
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Key to User for the sender
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Foreign Key to Conversation
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"Message from {self.sender.email} in {self.conversation.conversation_id}"

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['sent_at'] # Order messages by time sent
        # Optional: Add indexes for frequently filtered fields
        # indexes = [
        #     models.Index(fields=['sender']),
        #     models.Index(fields=['conversation']),
        #     models.Index(fields=['sent_at']),
        # ]
