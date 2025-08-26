from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Site information
    path('settings/', views.site_settings_view, name='site-settings'),
    path('health/', views.health_check_view, name='health-check'),
    path('info/', views.api_info_view, name='api-info'),
    
    # Contact and communication
    path('contact/', views.contact_message_view, name='contact'),
    path('newsletter/subscribe/', views.newsletter_subscribe_view, name='newsletter-subscribe'),
    path('newsletter/unsubscribe/', views.newsletter_unsubscribe_view, name='newsletter-unsubscribe'),
]