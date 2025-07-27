from rest_framework import permissions

class IsParticipantOrSender(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        if hasattr(obj, 'sender'):
            return obj.sender == user or user in obj.conversation.participants.all()
        return False