from rest_framework import viewsets, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .filters import MessageFilter
from .pagination import MessagePagination
from django.shortcuts import get_object_or_404
from .permissions import IsParticipantOfConversation

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']
    lookup_url_kwarg = 'conversation_id'

    def get_queryset(self):
        """Automatically add current user as participant when creating conversation"""
        return self.request.user.conversations.all()

    def create(self, serializer):
        """Automatically add current user as participant when creating conversation"""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = get_object_or_404(
            Conversation,
            pk=conversation_id,
            participants=request.user
        )

        serializer = MessageSerializer(data=request.data, context={
            'request': request,
            'conversation': conversation
        })
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body']
    lookup_url_kwarg = 'message_id'

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        if not conversation_id:
            raise Http404

        return Message.objects.filter(
            conversation__id=conversation_id,
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation').order_by('-sent_at')

    def get_conversation(self):
        """Helper method to get and validate the conversation"""
        return get_object_or_404(
            Conversation,
            pk=self.kwargs['conversation_pk'],
            participants=self.request.user
        )

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(
            Conversation,
            pk=conversation_id,
            participants=self.request.user
        )
        serializer.save(
            sender=self.request.user,
            conversation=self.get_conversation()
        )

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"detail": "You don't have permission to access this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)

