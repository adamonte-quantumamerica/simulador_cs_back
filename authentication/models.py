from django.contrib.auth.models import User
from django.db import models


# Comentado temporalmente para evitar conflictos
# class User(AbstractUser):
#     """
#     Usuario personalizado que usa email como identificador único
#     """
#     username = None  # Removemos el campo username
#     email = models.EmailField('Correo Electrónico', unique=True)
#     first_name = models.CharField('Nombre', max_length=30, blank=True)
#     last_name = models.CharField('Apellido', max_length=150, blank=True)
#     
#     # Configuración para usar email como username
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     
#     class Meta:
#         verbose_name = 'Usuario'
#         verbose_name_plural = 'Usuarios'
#     
#     def __str__(self):
#         return self.email


class ProjectAccess(models.Model):
    """
    Modelo para rastrear el acceso verificado de usuarios a proyectos
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_accesses')
    project = models.ForeignKey('projects.SolarProject', on_delete=models.CASCADE, related_name='user_accesses')
    granted_at = models.DateTimeField('Fecha de Acceso Concedido', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Acceso a Proyecto'
        verbose_name_plural = 'Accesos a Proyectos'
        unique_together = ['user', 'project']
        ordering = ['-granted_at']
    
    def __str__(self):
        return f"{self.user.email} -> {self.project.name}"