from django.urls import path
from .views import ASTUChatbotView

urlpatterns = [
    path('ask/', ASTUChatbotView.as_view(), name='chatbot-ask'),
]