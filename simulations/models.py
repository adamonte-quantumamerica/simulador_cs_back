from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from projects.models import SolarProject
import uuid

# Fixed energy price for savings calculation (legacy - use EnergyPrice model instead)
ENERGY_PRICE_ARS_PER_KWH = 101.25  # Updated price in ARS per kWh


class EnergyPrice(models.Model):
    """Model to store the current energy price configuration"""
    
    price_ars_per_kwh = models.DecimalField(
        'Precio de Energía (ARS por kWh)',
        max_digits=8,
        decimal_places=2,
        default=101.25,
        validators=[MinValueValidator(0)],
        help_text='Precio actual de la energía eléctrica en pesos argentinos por kWh'
    )
    description = models.CharField(
        'Descripción',
        max_length=200,
        blank=True,
        help_text='Descripción opcional del precio (ej: "Precio promedio nacional")'
    )
    effective_date = models.DateField(
        'Fecha de Vigencia',
        auto_now_add=False,
        help_text='Fecha desde la cual es efectivo este precio'
    )
    is_active = models.BooleanField(
        'Activo',
        default=True,
        help_text='Solo debe haber un precio activo a la vez'
    )
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última Actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Precio de Energía'
        verbose_name_plural = 'Precios de Energía'
        ordering = ['-effective_date']
    
    def __str__(self):
        return f"${self.price_ars_per_kwh} ARS/kWh - {self.effective_date}"
    
    @classmethod
    def get_current_price(cls):
        """Get the current active energy price"""
        try:
            active_price = cls.objects.filter(is_active=True).first()
            return active_price.price_ars_per_kwh if active_price else ENERGY_PRICE_ARS_PER_KWH
        except:
            return ENERGY_PRICE_ARS_PER_KWH
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate all other prices when this one is set as active
            EnergyPrice.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class TariffCategory(models.Model):
    """Model for simplified electricity tariff categories"""
    
    name = models.CharField('Nombre de la Categoría', max_length=100)
    code = models.CharField('Código', max_length=20, unique=True)
    description = models.TextField('Descripción', blank=True)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última Actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Categoría Tarifaria'
        verbose_name_plural = 'Categorías Tarifarias'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class ExchangeRate(models.Model):
    """Model to store USD/ARS exchange rates"""
    
    rate = models.DecimalField(
        'Tipo de Cambio (ARS por USD)', 
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    source = models.CharField('Fuente', max_length=100, default='Manual')
    date = models.DateField('Fecha')
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Tipo de Cambio'
        verbose_name_plural = 'Tipos de Cambio'
        ordering = ['-date']
        unique_together = ['date', 'source']
    
    def __str__(self):
        return f"USD/ARS {self.rate} - {self.date}"
    
    @classmethod
    def get_latest_rate(cls):
        """Get the most recent exchange rate"""
        latest = cls.objects.first()
        return latest.rate if latest else 1000  # Default fallback rate


class InvestmentSimulation(models.Model):
    """Model to store investment simulations"""
    
    SIMULATION_TYPE_CHOICES = [
        ('bill_coverage', 'Cobertura de Factura'),
        ('panels', 'Número de Paneles'),
        ('investment', 'Monto de Inversión'),
    ]
    
    # Unique identifier for the simulation
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Project and user information
    project = models.ForeignKey(SolarProject, on_delete=models.CASCADE, related_name='simulations')
    user = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE, 
        related_name='simulations',
        null=True,
        blank=True,
        help_text="Usuario autenticado (obligatorio para simulaciones persistidas)"
    )
    user_email = models.EmailField('Email del Usuario')  # Required
    user_phone = models.CharField('Teléfono del Usuario', max_length=20)  # Required, includes +54
    
    # Input parameters
    monthly_bill_ars = models.DecimalField(
        'Factura Mensual (ARS)', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    tariff_category = models.ForeignKey(TariffCategory, on_delete=models.CASCADE)
    
    simulation_type = models.CharField('Tipo de Simulación', max_length=20, choices=SIMULATION_TYPE_CHOICES)
    
    # Variable input (depends on simulation type)
    bill_coverage_percentage = models.DecimalField(
        'Porcentaje de Cobertura de Factura (%)', 
        max_digits=5, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    number_of_panels = models.PositiveIntegerField('Cantidad de Paneles', null=True, blank=True)
    investment_amount_usd = models.DecimalField(
        'Monto de Inversión (USD)', 
        max_digits=10, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    # Calculated results
    total_investment_usd = models.DecimalField(
        'Inversión Total (USD)', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    total_investment_ars = models.DecimalField(
        'Inversión Total (ARS)', 
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    installed_power_kw = models.DecimalField(
        'Potencia Instalada (kW)', 
        max_digits=8, 
        decimal_places=3,
        validators=[MinValueValidator(0)]
    )
    annual_generation_kwh = models.DecimalField(
        'Generación Anual (kWh)', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    monthly_generation_kwh = models.DecimalField(
        'Generación Mensual (kWh)', 
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    monthly_savings_ars = models.DecimalField(
        'Ahorro Mensual (ARS)', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    annual_savings_ars = models.DecimalField(
        'Ahorro Anual (ARS)', 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    payback_period_years = models.DecimalField(
        'Período de Retorno (años)', 
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Additional metrics
    bill_coverage_achieved = models.DecimalField(
        'Cobertura de Factura Lograda (%)', 
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    roi_annual = models.DecimalField(
        'ROI Anual (%)', 
        max_digits=6, 
        decimal_places=2
    )
    
    # Exchange rate used for calculation
    exchange_rate_used = models.DecimalField(
        'Tipo de Cambio Utilizado', 
        max_digits=8, 
        decimal_places=2
    )
    
    # Timestamps
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Simulación de Inversión'
        verbose_name_plural = 'Simulaciones de Inversión'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Simulación {self.id} - {self.project.name} ({self.simulation_type})"
    
    @property
    def monthly_savings_usd(self):
        """Calculate monthly savings in USD"""
        return self.monthly_savings_ars / self.exchange_rate_used
    
    @property
    def annual_savings_usd(self):
        """Calculate annual savings in USD using blue exchange rate: (monthly_savings_ars / exchange_rate) * 12"""
        return (self.monthly_savings_ars / self.exchange_rate_used) * 12
    
    @property
    def annual_savings_usd_legacy(self):
        """Calculate annual savings in USD using official exchange rate (legacy method)"""
        return self.annual_savings_ars / self.exchange_rate_used