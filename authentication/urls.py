from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [
    # Vistas básicas de autenticación
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('user/', views.current_user, name='current_user'),
    
    # URLs personalizadas para verificación de acceso a proyectos
    path('projects/<int:project_id>/verify-access/', views.verify_project_access, name='verify_project_access'),
    path('projects/<int:project_id>/check-access/', views.check_project_access, name='check_project_access'),
    path('user/project-accesses/', views.user_project_accesses, name='user_project_accesses'),
]
