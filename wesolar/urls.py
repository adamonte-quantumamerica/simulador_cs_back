"""
URL configuration for wesolar project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Simple favicon handler
def favicon_view(request):
    return HttpResponse(status=204)  # No Content

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Handle common browser requests to reduce warnings
    path('favicon.ico', favicon_view, name='favicon'),
    
    # Authentication endpoints
    path('auth/', include('authentication.urls')),
    
    # API endpoints
    path('api/v1/', include('projects.urls')),
    path('api/v1/', include('simulations.urls')),
    path('api/v1/', include('core.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)