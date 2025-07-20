from rest_framework import status
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

# Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing conversation instances.
    Allows listing all conversations and creating new ones.
    """
    queryset = Conversation.objects.all().order_by('-created_at') # Order by most recent
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated] # Ensures only authenticated users can access

    def get_queryset(self):
        """
        Optionally restricts the returned conversations to those
        that the current user is a participant of.
        """
        user = self.request.user
        # Return conversations where the current user is a participant
        return Conversation.objects.filter(participants=user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Custom create method to ensure the current user is added as a participant
        if not explicitly included, and to handle many-to-many participants.
        """
        # The serializer's create method will handle the 'participants' field
        # due to `source='participants'` in `participant_ids` in the serializer.
        # However, we can add the current user explicitly if needed.
        conversation = serializer.save()
        # Ensure the creating user is a participant
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)
        conversation.save()

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Retrieves all messages for a specific conversation.
        URL: /conversations/{conversation_id}/messages/
        """
        conversation = get_object_or_404(Conversation, pk=pk)
        # Ensure the requesting user is a participant of this conversation
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        messages = conversation.messages.all().order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Sends a new message to an existing conversation.
        URL: /conversations/{conversation_id}/send_message/
        """
        conversation = get_object_or_404(Conversation, pk=pk)
        # Ensure the requesting user is a participant of this conversation
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Prepare data for the MessageSerializer
        # The sender is the current authenticated user
        # The conversation is the one identified by 'pk'
        data = request.data.copy()
        data['sender_id'] = request.user.user_id # Set sender to current user's ID
        data['conversation'] = conversation.conversation_id # Set conversation ID

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            # Save the message, linking it to the current user and conversation
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Message ViewSet (primarily for individual message operations if needed)
# For listing messages within a conversation, the @action on ConversationViewSet is preferred.
class MessageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing message instances.
    Primarily used for retrieving, updating, or deleting individual messages.
    Listing messages is typically handled via the ConversationViewSet's 'messages' action.
    """
    queryset = Message.objects.all().order_by('sent_at')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Allows filtering messages by sender or conversation if query parameters are provided.
        Example: /messages/?sender_id=<uuid> or /messages/?conversation_id=<uuid>
        """
        queryset = super().get_queryset()
        sender_id = self.request.query_params.get('sender_id')
        conversation_id = self.request.query_params.get('conversation_id')

        if sender_id:
            queryset = queryset.filter(sender__user_id=sender_id)
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)

        return queryset

    def perform_create(self, serializer):
        """
        Ensures the sender of the message is the authenticated user.
        """
        # The sender_id field in the serializer handles linking the sender.
        # We ensure it's the current user for security.
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        """
        Ensures only the sender can update their message.
        """
        if self.request.user != serializer.instance.sender:
            return Response(
                {"detail": "You do not have permission to edit this message."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        """
        Ensures only the sender can delete their message.
        """
        if self.request.user != instance.sender:
            return Response(
                {"detail": "You do not have permission to delete this message."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()