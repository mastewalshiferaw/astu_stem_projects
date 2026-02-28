from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SecurityLogViewSet, RegisterView

router = DefaultRouter()
router.register(r'security-logs', SecurityLogViewSet, basename='security-log')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]