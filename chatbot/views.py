from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status,serializers
from rest_framework.throttling import UserRateThrottle
from .models import ChatHistory
from .utils import get_astu_ai_response
from drf_spectacular.utils import extend_schema

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="The question you want to ask the ASTU Assistant")



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

 @extend_schema(request=ChatRequestSerializer, responses={200: dict})
    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_query = serializer.validated_data.get('message')
            bot_response = get_astu_ai_response(user_query)
            
            ChatHistory.objects.create(
                user=request.user,
                message=user_query,
                response=bot_response
            )
            return Response({"query": user_query, "response": bot_response})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)