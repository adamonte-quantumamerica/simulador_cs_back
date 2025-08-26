from django.contrib import admin
from .models import ContactMessage, SiteSettings, Newsletter

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    list_editable = ['is_read']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        # Messages are created through the API
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Información Básica', {
            'fields': ['site_name', 'site_description']
        }),
        ('Información de Contacto', {
            'fields': ['contact_email', 'contact_phone', 'address']
        }),
        ('Redes Sociales', {
            'fields': ['facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url'],
            'classes': ['collapse']
        }),
        ('SEO y Analytics', {
            'fields': ['meta_keywords', 'google_analytics_id'],
            'classes': ['collapse']
        }),
        ('Configuración de Cálculos', {
            'fields': ['default_annual_generation_factor', 'default_performance_ratio'],
            'classes': ['collapse']
        }),
        ('Metadatos', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of site settings
        return False


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']
    list_editable = ['is_active']
    ordering = ['-subscribed_at']