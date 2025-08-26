from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import os


def project_image_path(instance, filename):
    """Generate file path for project images"""
    return f'projects/{instance.id}/images/{filename}'


def project_video_path(instance, filename):
    """Generate file path for project videos"""
    return f'projects/{instance.id}/videos/{filename}'


class SolarProject(models.Model):
    """Model representing a community solar project"""
    
    STATUS_CHOICES = [
        ('development', 'En Desarrollo'),
        ('funding', 'En Financiamiento'),
        ('construction', 'En Construcción'),
        ('operational', 'Operativo'),
        ('completed', 'Completado'),
    ]
    
    # Basic information
    name = models.CharField('Nombre del Proyecto', max_length=200)
    description = models.TextField('Descripción')
    location = models.CharField('Ubicación', max_length=200)
    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default='development')
    
    # Technical specifications
    total_power_installed = models.DecimalField(
        'Potencia Total Instalada (kWp)', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    total_power_projected = models.DecimalField(
        'Potencia Total Proyectada (kWp)', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    available_power = models.DecimalField(
        'Potencia Disponible (kWp)', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Financial information
    price_per_wp_usd = models.DecimalField(
        'Precio por Wp (USD)', 
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    price_per_panel_usd = models.DecimalField(
        'Precio por Panel (USD)', 
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    panel_power_wp = models.DecimalField(
        'Potencia por Panel (Wp)', 
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=550  # Typical panel power
    )
    
    # Project details
    owners = models.TextField('Propietarios', help_text='Separar múltiples propietarios con comas')
    expected_annual_generation = models.DecimalField(
        'Generación Anual Esperada (kWh)', 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    
    # Access control
    financial_access_password = models.CharField(
        'Contraseña de Acceso Financiero', 
        max_length=50,
        default='iris2025',
        help_text='Contraseña requerida para acceder a información financiera y simulador'
    )
    
    # Commercial contact
    commercial_whatsapp = models.CharField(
        'WhatsApp Comercial',
        max_length=20,
        blank=True,
        help_text='Número de WhatsApp para contacto comercial (ej: +541112345678)'
    )
    
    # Crowdfunding information (for future use)
    funding_goal = models.DecimalField(
        'Meta de Financiamiento (USD)', 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    funding_raised = models.DecimalField(
        'Financiamiento Recaudado (USD)', 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    funding_deadline = models.DateField('Fecha Límite de Financiamiento', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última Actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Proyecto Solar'
        verbose_name_plural = 'Proyectos Solares'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def funding_percentage(self):
        """Calculate funding percentage"""
        if self.funding_goal and self.funding_goal > 0:
            return min((self.funding_raised / self.funding_goal) * 100, 100)
        return 0
    
    @property
    def available_power_percentage(self):
        """Calculate available power percentage"""
        if self.total_power_projected and self.total_power_projected > 0:
            return (self.available_power / self.total_power_projected) * 100
        return 0


class ProjectImage(models.Model):
    """Model for project images"""
    project = models.ForeignKey(SolarProject, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Imagen', upload_to=project_image_path)
    caption = models.CharField('Descripción', max_length=200, blank=True)
    is_featured = models.BooleanField('Imagen Principal', default=False)
    order = models.PositiveIntegerField('Orden', default=0)
    
    class Meta:
        verbose_name = 'Imagen del Proyecto'
        verbose_name_plural = 'Imágenes del Proyecto'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.project.name} - Imagen {self.id}"


class ProjectVideo(models.Model):
    """Model for project videos"""
    project = models.ForeignKey(SolarProject, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField('Video', upload_to=project_video_path, null=True, blank=True)
    video_url = models.URLField('URL del Video', blank=True, help_text='URL de YouTube, Vimeo, etc.')
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción', blank=True)
    order = models.PositiveIntegerField('Orden', default=0)
    
    class Meta:
        verbose_name = 'Video del Proyecto'
        verbose_name_plural = 'Videos del Proyecto'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.project.name} - {self.title}"