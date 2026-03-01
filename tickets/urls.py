from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, AdminAnalyticsView

router = DefaultRouter()
router.register(r'', TicketViewSet, basename='ticket')

urlpatterns = [
    path('analytics/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('', include(router.urls)),
]