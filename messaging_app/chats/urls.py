from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from . import views

# Base router for conversations
router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', views.MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
