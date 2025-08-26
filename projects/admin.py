from django.contrib import admin
from .models import SolarProject, ProjectImage, ProjectVideo


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'is_featured', 'order']


class ProjectVideoInline(admin.TabularInline):
    model = ProjectVideo
    extra = 1
    fields = ['title', 'video', 'video_url', 'description', 'order']


@admin.register(SolarProject)
class SolarProjectAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'location', 'status', 'available_power', 
        'price_per_wp_usd', 'funding_percentage', 'created_at'
    ]
    list_filter = ['status', 'location', 'created_at']
    search_fields = ['name', 'description', 'location', 'owners']
    readonly_fields = ['funding_percentage', 'available_power_percentage', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Información Básica', {
            'fields': ['name', 'description', 'location', 'status', 'owners']
        }),
        ('Especificaciones Técnicas', {
            'fields': [
                'total_power_installed', 'total_power_projected', 'available_power',
                'panel_power_wp', 'expected_annual_generation', 'available_power_percentage'
            ]
        }),
        ('Información Financiera', {
            'fields': [
                'price_per_wp_usd', 'price_per_panel_usd', 
                'funding_goal', 'funding_raised', 'funding_deadline', 'funding_percentage'
            ]
        }),
        ('Control de Acceso', {
            'fields': ['financial_access_password'],
            'description': 'Contraseña requerida para acceder a la información financiera y simulador de inversión.'
        }),
        ('Contacto Comercial', {
            'fields': ['commercial_whatsapp'],
            'description': 'Número de WhatsApp para contacto comercial y asesoramiento.'
        }),
        ('Metadatos', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    inlines = [ProjectImageInline, ProjectVideoInline]
    
    def funding_percentage(self, obj):
        return f"{obj.funding_percentage:.1f}%"
    funding_percentage.short_description = 'Financiamiento (%)'


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'is_featured', 'order']
    list_filter = ['is_featured', 'project']
    list_editable = ['is_featured', 'order']


@admin.register(ProjectVideo)
class ProjectVideoAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'order']
    list_filter = ['project']
    list_editable = ['order']