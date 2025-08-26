from django.db import models


class ContactMessage(models.Model):
    """Model for storing contact form messages"""
    
    name = models.CharField('Nombre', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    subject = models.CharField('Asunto', max_length=200)
    message = models.TextField('Mensaje')
    is_read = models.BooleanField('Leído', default=False)
    created_at = models.DateTimeField('Fecha de Envío', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class SiteSettings(models.Model):
    """Model for storing site-wide settings"""
    
    site_name = models.CharField('Nombre del Sitio', max_length=100, default='Simulador CS')
    site_description = models.TextField('Descripción del Sitio', blank=True)
    contact_email = models.EmailField('Email de Contacto', blank=True)
    contact_phone = models.CharField('Teléfono de Contacto', max_length=20, blank=True)
    address = models.TextField('Dirección', blank=True)
    
    # Social media links
    facebook_url = models.URLField('Facebook', blank=True)
    twitter_url = models.URLField('Twitter', blank=True)
    linkedin_url = models.URLField('LinkedIn', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    
    # SEO settings
    meta_keywords = models.TextField('Palabras Clave SEO', blank=True)
    google_analytics_id = models.CharField('Google Analytics ID', max_length=50, blank=True)
    
    # Default values for calculations
    default_annual_generation_factor = models.DecimalField(
        'Factor de Generación Anual por Defecto (kWh/kWp)', 
        max_digits=6, 
        decimal_places=2,
        default=1500,
        help_text='Generación anual promedio por kWp instalado'
    )
    default_performance_ratio = models.DecimalField(
        'Ratio de Performance por Defecto', 
        max_digits=4, 
        decimal_places=3,
        default=0.85,
        help_text='Eficiencia del sistema (0.0 - 1.0)'
    )
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última Actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Configuración del Sitio'
        verbose_name_plural = 'Configuraciones del Sitio'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Solo puede existir una instancia de configuración del sitio')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get the site settings instance, create if doesn't exist"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Simulador CS',
                'site_description': 'Plataforma de simulación y cotización de inversiones en Comunidades Solares'
            }
        )
        return settings


class Newsletter(models.Model):
    """Model for newsletter subscriptions"""
    
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Nombre', max_length=100, blank=True)
    is_active = models.BooleanField('Activo', default=True)
    subscribed_at = models.DateTimeField('Fecha de Suscripción', auto_now_add=True)
    unsubscribed_at = models.DateTimeField('Fecha de Baja', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Suscripción a Newsletter'
        verbose_name_plural = 'Suscripciones a Newsletter'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email