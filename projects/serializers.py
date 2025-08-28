from rest_framework import serializers
from .models import SolarProject, ProjectImage, ProjectVideo


class ProjectImageSerializer(serializers.ModelSerializer):
    """Serializer for project images"""
    image_path = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectImage
        fields = ['id', 'image_path', 'caption', 'is_featured', 'order']
    
    def get_image_path(self, obj):
        """Return relative path instead of absolute URL"""
        return obj.image.name if obj.image else None


class ProjectVideoSerializer(serializers.ModelSerializer):
    """Serializer for project videos"""
    
    class Meta:
        model = ProjectVideo
        fields = ['id', 'video', 'video_url', 'title', 'description', 'order']


class SolarProjectListSerializer(serializers.ModelSerializer):
    """Serializer for solar project list view (minimal fields)"""
    
    featured_image = serializers.SerializerMethodField()
    funding_percentage = serializers.ReadOnlyField()
    available_power_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = SolarProject
        fields = [
            'id', 'name', 'location', 'status', 'available_power', 
            'total_power_projected', 'price_per_wp_usd', 'featured_image',
            'funding_percentage', 'available_power_percentage', 'created_at'
        ]
    
    def get_featured_image(self, obj):
        """Get the featured image path (relative)"""
        featured_image = obj.images.filter(is_featured=True).first()
        if featured_image:
            # Devolver solo el path relativo, no URL absoluta del backend
            # El frontend construirá la URL completa
            return featured_image.image.name if featured_image.image else None
        return None


class SolarProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer for solar project detail view (all fields)"""
    
    images = ProjectImageSerializer(many=True, read_only=True)
    videos = ProjectVideoSerializer(many=True, read_only=True)
    funding_percentage = serializers.ReadOnlyField()
    available_power_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = SolarProject
        fields = [
            'id', 'name', 'description', 'location', 'status',
            'total_power_installed', 'total_power_projected', 'available_power',
            'price_per_wp_usd', 'price_per_panel_usd', 'panel_power_wp',
            'owners', 'expected_annual_generation', 'funding_goal', 
            'funding_raised', 'funding_deadline', 'funding_percentage',
            'available_power_percentage', 'financial_access_password', 'commercial_whatsapp', 'images', 'videos',
            'created_at', 'updated_at'
        ]


class SolarProjectCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating solar projects"""
    
    class Meta:
        model = SolarProject
        fields = [
            'name', 'description', 'location', 'status',
            'total_power_installed', 'total_power_projected', 'available_power',
            'price_per_wp_usd', 'price_per_panel_usd', 'panel_power_wp',
            'owners', 'expected_annual_generation', 'funding_goal', 
            'funding_raised', 'funding_deadline'
        ]
    
    def validate_available_power(self, value):
        """Validate that available power doesn't exceed total projected power"""
        total_power_projected = self.initial_data.get('total_power_projected')
        if total_power_projected and value > float(total_power_projected):
            raise serializers.ValidationError(
                "La potencia disponible no puede ser mayor a la potencia total proyectada."
            )
        return value
    
    def validate_funding_raised(self, value):
        """Validate that funding raised doesn't exceed funding goal"""
        funding_goal = self.initial_data.get('funding_goal')
        if funding_goal and value > float(funding_goal):
            raise serializers.ValidationError(
                "El financiamiento recaudado no puede ser mayor a la meta de financiamiento."
            )
        return value


class SolarProjectFinancialSerializer(serializers.ModelSerializer):
    """
    Serializer para información financiera protegida de un proyecto
    """
    funding_percentage = serializers.ReadOnlyField()
    available_power_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = SolarProject
        fields = [
            'id', 'name', 'price_per_wp_usd', 'price_per_panel_usd', 'panel_power_wp',
            'funding_goal', 'funding_raised', 'funding_deadline', 'funding_percentage',
            'available_power', 'total_power_projected', 'available_power_percentage',
            'expected_annual_generation', 'commercial_whatsapp'
        ]


class SolarProjectSimulatorConfigSerializer(serializers.ModelSerializer):
    """
    Serializer para la configuración del simulador de un proyecto
    """
    class Meta:
        model = SolarProject
        fields = [
            'id', 'name', 'available_power', 'total_power_projected',
            'price_per_wp_usd', 'price_per_panel_usd', 'panel_power_wp',
            'expected_annual_generation'
        ]