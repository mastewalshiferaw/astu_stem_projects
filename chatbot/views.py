from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.throttling import UserRateThrottle
from .models import ChatHistory
from .utils import get_astu_ai_response

class ChatbotThrottle(UserRateThrottle):
    rate = '10/minute'



class ASTUChatbotView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ChatbotThrottle]

    def post(self, request):
        user_query = request.data.get('message')
        
        if not user_query:
            return Response({"error": "Message is required"}, status=400)

        # Get AI Response
        bot_response = get_astu_ai_response(user_query)

        # Save to history for Admin analytics
        ChatHistory.objects.create(
            user=request.user,
            message=user_query,
            response=bot_response
        )

        return Response({
            "query": user_query,
            "response": bot_response
        })