from django.contrib import admin
from .models import InvestmentSimulation, TariffCategory, ExchangeRate, EnergyPrice


@admin.register(EnergyPrice)
class EnergyPriceAdmin(admin.ModelAdmin):
    list_display = ['price_ars_per_kwh', 'description', 'effective_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'effective_date', 'created_at']
    search_fields = ['description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    ordering = ['-effective_date']
    
    fieldsets = [
        ('Configuración del Precio', {
            'fields': ['price_ars_per_kwh', 'description', 'effective_date', 'is_active'],
            'description': 'Configure el precio actual de la energía eléctrica. Solo debe haber un precio activo a la vez.'
        }),
        ('Metadatos', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    def get_queryset(self, request):
        # Show active price first
        return super().get_queryset(request).order_by('-is_active', '-effective_date')


@admin.register(TariffCategory)
class TariffCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Información Básica', {
            'fields': ['name', 'code', 'description']
        }),
        ('Metadatos', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['date', 'rate', 'source', 'created_at']
    list_filter = ['source', 'date']
    search_fields = ['source']
    readonly_fields = ['created_at']
    ordering = ['-date']


@admin.register(InvestmentSimulation)
class InvestmentSimulationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'project', 'simulation_type', 'total_investment_usd',
        'monthly_savings_ars', 'payback_period_years', 'roi_annual', 'created_at'
    ]
    list_filter = ['simulation_type', 'project', 'created_at', 'tariff_category']
    search_fields = ['project__name', 'user_email', 'user_phone', 'id']
    readonly_fields = [
        'id', 'total_investment_usd', 'total_investment_ars',
        'installed_power_kw', 'annual_generation_kwh', 'monthly_generation_kwh',
        'monthly_savings_ars', 'annual_savings_ars', 'payback_period_years',
        'bill_coverage_achieved', 'roi_annual', 'exchange_rate_used', 'created_at'
    ]
    
    fieldsets = [
        ('Información del Usuario', {
            'fields': ['id', 'user_email', 'user_phone', 'created_at']
        }),
        ('Información del Proyecto', {
            'fields': ['project', 'tariff_category']
        }),
        ('Parámetros de Entrada', {
            'fields': [
                'monthly_bill_ars', 'simulation_type',
                'bill_coverage_percentage', 'number_of_panels', 'investment_amount_usd'
            ]
        }),
        ('Resultados de la Simulación', {
            'fields': [
                'total_investment_usd', 'total_investment_ars',
                'installed_power_kw', 'annual_generation_kwh', 'monthly_generation_kwh',
                'monthly_savings_ars', 'annual_savings_ars', 'payback_period_years',
                'bill_coverage_achieved', 'roi_annual', 'exchange_rate_used'
            ],
            'classes': ['collapse']
        })
    ]
    
    def has_add_permission(self, request):
        # Prevent manual creation of simulations in admin
        return False
    
    def has_change_permission(self, request, obj=None):
        # Make simulations read-only in admin
        return False