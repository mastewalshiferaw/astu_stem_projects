from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # All ticket related routes (tickets, analytics)
    path('api/tickets/', include('tickets.urls')),
    
    # All account related routes (register, security-logs)
    path('api/accounts/', include('accounts.urls')),
    
    # Chatbot and Notifications
    path('api/chatbot/', include('chatbot.urls')),
    path('api/notifications/', include('notifications.urls')),
    
    # JWT Auth
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger Documentation
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)