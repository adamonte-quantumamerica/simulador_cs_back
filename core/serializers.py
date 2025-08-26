from rest_framework import serializers
from .models import ContactMessage, SiteSettings, Newsletter


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for contact messages"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        
    def validate_message(self, value):
        """Validate message length"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "El mensaje debe tener al menos 10 caracteres."
            )
        return value


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Serializer for site settings"""
    
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_description', 'contact_email', 'contact_phone',
            'address', 'facebook_url', 'twitter_url', 'linkedin_url', 
            'instagram_url', 'meta_keywords'
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    """Serializer for newsletter subscriptions"""
    
    class Meta:
        model = Newsletter
        fields = ['email', 'name']
        
    def validate_email(self, value):
        """Additional email validation"""
        if not value or '@' not in value:
            raise serializers.ValidationError(
                "Ingrese un email válido."
            )
        return value.lower().strip()


class NewsletterStatusSerializer(serializers.ModelSerializer):
    """Serializer for newsletter status (with timestamps)"""
    
    class Meta:
        model = Newsletter
        fields = ['email', 'name', 'is_active', 'subscribed_at', 'unsubscribed_at']
        read_only_fields = ['subscribed_at', 'unsubscribed_at']