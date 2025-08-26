from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import ContactMessage, SiteSettings, Newsletter
from .serializers import ContactMessageSerializer, SiteSettingsSerializer, NewsletterSerializer


@api_view(['GET'])
def site_settings_view(request):
    """
    API view to get site settings
    """
    try:
        settings_obj = SiteSettings.get_settings()
        serializer = SiteSettingsSerializer(settings_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Error al obtener configuración del sitio'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def contact_message_view(request):
    """
    API view to create a contact message
    """
    serializer = ContactMessageSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            # Save the contact message
            contact_message = serializer.save()
            
            # Send email notification (optional)
            if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
                try:
                    site_settings = SiteSettings.get_settings()
                    send_mail(
                        subject=f'Nuevo mensaje de contacto: {contact_message.subject}',
                        message=f"""
                        Nuevo mensaje de contacto recibido:
                        
                        Nombre: {contact_message.name}
                        Email: {contact_message.email}
                        Teléfono: {contact_message.phone}
                        Asunto: {contact_message.subject}
                        
                        Mensaje:
                        {contact_message.message}
                        """,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[site_settings.contact_email] if site_settings.contact_email else [settings.DEFAULT_FROM_EMAIL],
                        fail_silently=True,
                    )
                except Exception as email_error:
                    # Log email error but don't fail the request
                    print(f"Error sending email: {email_error}")
            
            return Response({
                'message': 'Mensaje enviado correctamente',
                'success': True
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': f'Error al enviar el mensaje: {str(e)}',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'errors': serializer.errors,
        'success': False
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def newsletter_subscribe_view(request):
    """
    API view to subscribe to newsletter
    """
    serializer = NewsletterSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            # Check if email already exists
            email = serializer.validated_data['email']
            subscription, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={
                    'name': serializer.validated_data.get('name', ''),
                    'is_active': True
                }
            )
            
            if created:
                message = 'Suscripción exitosa al newsletter'
                status_code = status.HTTP_201_CREATED
            else:
                if subscription.is_active:
                    message = 'Ya estás suscrito al newsletter'
                    status_code = status.HTTP_200_OK
                else:
                    # Reactivate subscription
                    subscription.is_active = True
                    subscription.unsubscribed_at = None
                    subscription.save()
                    message = 'Suscripción reactivada exitosamente'
                    status_code = status.HTTP_200_OK
            
            return Response({
                'message': message,
                'success': True
            }, status=status_code)
            
        except Exception as e:
            return Response({
                'error': f'Error al suscribirse: {str(e)}',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'errors': serializer.errors,
        'success': False
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def newsletter_unsubscribe_view(request):
    """
    API view to unsubscribe from newsletter
    """
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email es requerido',
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        subscription = Newsletter.objects.get(email=email, is_active=True)
        subscription.is_active = False
        subscription.unsubscribed_at = timezone.now()
        subscription.save()
        
        return Response({
            'message': 'Te has dado de baja del newsletter exitosamente',
            'success': True
        }, status=status.HTTP_200_OK)
        
    except Newsletter.DoesNotExist:
        return Response({
            'error': 'No se encontró una suscripción activa con ese email',
            'success': False
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Error al darse de baja: {str(e)}',
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def health_check_view(request):
    """
    API view for health check
    """
    return Response({
        'status': 'healthy',
        'message': 'WeSolar API is running',
        'version': '1.0.0'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_info_view(request):
    """
    API view to get general API information
    """
    from projects.models import SolarProject
    from simulations.models import InvestmentSimulation, TariffCategory
    
    try:
        stats = {
            'api_version': '1.0.0',
            'total_projects': SolarProject.objects.count(),
            'total_simulations': InvestmentSimulation.objects.count(),
            'available_tariff_categories': TariffCategory.objects.count(),
            'endpoints': {
                'projects': '/api/v1/projects/',
                'simulations': '/api/v1/simulations/create/',
                'tariff_categories': '/api/v1/tariff-categories/',
                'contact': '/api/v1/contact/',
                'newsletter': '/api/v1/newsletter/subscribe/',
                'docs': '/api/docs/'
            }
        }
        
        return Response(stats, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Error al obtener información de la API'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)