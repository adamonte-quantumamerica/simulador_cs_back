"""
URL configuration for wesolar project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Simple handlers for common requests
def favicon_view(request):
    return HttpResponse(status=204)  # No Content

def root_view(request):
    """Simple root endpoint with API information"""
    return JsonResponse({
        'message': 'WeSolar API',
        'version': '1.0.0',
        'docs': '/api/docs/',
        'admin': '/admin/'
    })

# Redirect handlers for URLs missing /api/v1/ prefix
def redirect_projects_stats(request):
    return redirect('/api/v1/projects/stats/')

def redirect_simulations_stats(request):
    return redirect('/api/v1/simulations/stats/')

def redirect_exchange_rate(request):
    return redirect('/api/v1/exchange-rate/current/')

def redirect_settings(request):
    return redirect('/api/v1/settings/')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Root endpoint
    path('', root_view, name='root'),
    
    # Handle common browser requests to reduce warnings
    path('favicon.ico', favicon_view, name='favicon'),
    path('favicon.png', favicon_view, name='favicon-png'),
    
    # Redirect URLs missing /api/v1/ prefix (help frontend)
    path('projects/stats/', redirect_projects_stats, name='redirect-projects-stats'),
    path('simulations/stats/', redirect_simulations_stats, name='redirect-simulations-stats'),
    path('exchange-rate/current/', redirect_exchange_rate, name='redirect-exchange-rate'),
    path('settings/', redirect_settings, name='redirect-settings'),
    
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