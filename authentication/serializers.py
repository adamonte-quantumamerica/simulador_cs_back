from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import ProjectAccess
from projects.models import SolarProject


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de usuarios
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para información del usuario
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')


class ProjectAccessVerificationSerializer(serializers.Serializer):
    """
    Serializer para verificar el código de acceso a un proyecto
    """
    access_code = serializers.CharField(
        max_length=50,
        help_text="Código de acceso al proyecto"
    )
    
    def validate_access_code(self, value):
        """
        Valida que el código de acceso sea correcto para el proyecto
        """
        project_id = self.context.get('project_id')
        if not project_id:
            raise serializers.ValidationError("ID del proyecto requerido")
        
        try:
            project = SolarProject.objects.get(id=project_id)
        except SolarProject.DoesNotExist:
            raise serializers.ValidationError("Proyecto no encontrado")
        
        # Verificar si el código de acceso es correcto
        if not check_password(value, project.financial_access_password) and value != project.financial_access_password:
            raise serializers.ValidationError("Código de acceso incorrecto")
        
        return value


class ProjectAccessSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ProjectAccess
    """
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = ProjectAccess
        fields = ('id', 'project', 'project_name', 'granted_at')
        read_only_fields = ('granted_at',)
