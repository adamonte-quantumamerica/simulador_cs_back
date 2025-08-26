from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
# from django_ratelimit.decorators import ratelimit  # Comentado por problemas de entorno
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .models import ProjectAccess
from .serializers import ProjectAccessVerificationSerializer, ProjectAccessSerializer, UserCreateSerializer, UserSerializer
from projects.models import SolarProject


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
# @ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)  # Comentado por problemas de entorno
@never_cache
def verify_project_access(request, project_id):
    """
    Verificar el código de acceso para un proyecto específico
    """
    try:
        project = get_object_or_404(SolarProject, id=project_id)
        
        serializer = ProjectAccessVerificationSerializer(
            data=request.data,
            context={'project_id': project_id}
        )
        
        if serializer.is_valid():
            access_code = serializer.validated_data['access_code']
            
            # Verificar si el código es correcto (soporta tanto texto plano como hash)
            is_valid = (
                check_password(access_code, project.financial_access_password) or
                access_code == project.financial_access_password
            )
            
            if is_valid:
                # Crear o obtener el registro de acceso
                project_access, created = ProjectAccess.objects.get_or_create(
                    user=request.user,
                    project=project
                )
                
                return Response(
                    {
                        'message': 'Acceso verificado correctamente',
                        'project_name': project.name,
                        'granted_at': project_access.granted_at
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Código de acceso incorrecto'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {'error': 'Error interno del servidor'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_project_accesses(request):
    """
    Obtener todos los accesos a proyectos del usuario autenticado
    """
    try:
        accesses = ProjectAccess.objects.filter(user=request.user).select_related('project')
        serializer = ProjectAccessSerializer(accesses, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': 'Error al obtener accesos a proyectos'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_project_access(request, project_id):
    """
    Verificar si el usuario tiene acceso a un proyecto específico
    """
    try:
        project = get_object_or_404(SolarProject, id=project_id)
        
        has_access = ProjectAccess.objects.filter(
            user=request.user,
            project=project
        ).exists()
        
        return Response(
            {
                'has_access': has_access,
                'project_name': project.name
            },
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        return Response(
            {'error': 'Error al verificar acceso al proyecto'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """
    Registro de nuevos usuarios
    """
    try:
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Crear token para el usuario
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'Usuario registrado exitosamente'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {'error': 'Error al registrar usuario'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    """
    Login de usuarios
    """
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username y password son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user:
            # Crear o obtener token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'Login exitoso'
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    except Exception as e:
        return Response(
            {'error': 'Error en el login'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    """
    Logout de usuarios
    """
    try:
        # Eliminar el token del usuario
        request.user.auth_token.delete()
        
        return Response(
            {'message': 'Logout exitoso'},
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        return Response(
            {'error': 'Error en el logout'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Obtener información del usuario actual
    """
    try:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': 'Error al obtener información del usuario'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )