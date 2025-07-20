from rest_framework import serializers
from .models import User, Conversation, Message

# A simple User serializer for nesting within other serializers
# This avoids including sensitive info like password and prevents circular imports
class UserSerializer(serializers.ModelSerializer):
    # Example of serializers.SerializerMethodField to add a custom computed field
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'full_name']
        read_only_fields = ['user_id', 'email', 'role', 'full_name'] # user_id, email, role, and full_name are read-only

    def get_full_name(self, obj):
        """
        Returns the full name of the user.
        """
        return f"{obj.first_name} {obj.last_name}"

    def validate_phone_number(self, value):
        """
        Example of custom validation using serializers.ValidationError.
        Ensures the phone number, if provided, is numeric.
        """
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        # You could add more complex validation here, e.g., length checks, regex patterns
        return value

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    # Display the sender's details when retrieving messages
    # Use the simple UserSerializer for nesting
    sender = UserSerializer(read_only=True)

    # When creating/updating a message, allow specifying sender by their user_id
    # This field will be used for writing, while the above 'sender' is for reading
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='sender', write_only=True
    )

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_id', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at'] # These fields are set automatically

# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    # Display participants using the UserSerializer for nesting
    # many=True because it's a ManyToMany relationship
    participants = UserSerializer(many=True, read_only=True)

    # Allow specifying participants by their user_ids when creating/updating a conversation
    # write_only=True ensures this field is only used for input, not output
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), source='participants', write_only=True
    )

    # Nested messages within the conversation
    # read_only=True because messages are created separately and linked to a conversation
    # many=True because there can be multiple messages in a conversation
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at'] # These fields are set automatically
