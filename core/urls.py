from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Import your ViewSets here
from tickets.views import TicketViewSet
from accounts.views import SecurityLogViewSet
from notifications.views import NotificationViewSet

# 1. Create ONE central router
router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'security-logs', SecurityLogViewSet, basename='security-log')
router.register(r'notifications', NotificationViewSet, basename='notification')

# Import Auth and Swagger views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. Include the central router once
    path('api/', include(router.urls)),
    
    # 3. Include manual paths from apps
    path('api/tickets/', include('tickets.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    
    # 4. Auth & Docs
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)