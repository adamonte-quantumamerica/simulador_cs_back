"""
URL configuration for wesolar project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
import os

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
def redirect_projects(request):
    # Mantener los query parameters (como ?search=)
    query_string = request.GET.urlencode()
    redirect_url = '/api/v1/projects/'
    if query_string:
        redirect_url += '?' + query_string
    return redirect(redirect_url)

def redirect_projects_stats(request):
    return redirect('/api/v1/projects/stats/')

def redirect_simulations_stats(request):
    return redirect('/api/v1/simulations/stats/')

def redirect_exchange_rate(request):
    return redirect('/api/v1/exchange-rate/current/')

def redirect_settings(request):
    return redirect('/api/v1/settings/')

def redirect_simulations(request):
    # Mantener los query parameters
    query_string = request.GET.urlencode()
    redirect_url = '/api/v1/simulations/'
    if query_string:
        redirect_url += '?' + query_string
    return redirect(redirect_url)

def redirect_exchange_rates(request):
    return redirect('/api/v1/exchange-rates/')

def redirect_tariff_categories(request):
    return redirect('/api/v1/tariff-categories/')

def redirect_project_detail(request, project_id):
    return redirect(f'/api/v1/projects/{project_id}/')

def serve_media(request, path):
    """Custom media file server for Vercel"""
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(media_path) and os.path.isfile(media_path):
        return FileResponse(open(media_path, 'rb'))
    raise Http404("Media file not found")

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Custom media server (must be FIRST to avoid conflicts)
    path('media/<path:path>', serve_media, name='media'),
    
    # Root endpoint
    path('', root_view, name='root'),
    
    # Handle common browser requests to reduce warnings
    path('favicon.ico', favicon_view, name='favicon'),
    path('favicon.png', favicon_view, name='favicon-png'),
    
    # Redirect URLs missing /api/v1/ prefix (help frontend)
    path('projects/', redirect_projects, name='redirect-projects'),
    path('projects/<int:project_id>/', redirect_project_detail, name='redirect-project-detail'),
    path('projects/stats/', redirect_projects_stats, name='redirect-projects-stats'),
    path('simulations/', redirect_simulations, name='redirect-simulations'),
    path('simulations/stats/', redirect_simulations_stats, name='redirect-simulations-stats'),
    path('tariff-categories/', redirect_tariff_categories, name='redirect-tariff-categories'),
    path('exchange-rate/current/', redirect_exchange_rate, name='redirect-exchange-rate'),
    path('exchange-rates/', redirect_exchange_rates, name='redirect-exchange-rates'),
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

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)