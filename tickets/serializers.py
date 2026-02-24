from rest_framework import serializers
from .models import Ticket, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'author', 'author_name', 'status', 'attachment', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'status'] 