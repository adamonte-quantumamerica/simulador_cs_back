from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Public endpoints
    path('projects/', views.SolarProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.SolarProjectDetailView.as_view(), name='project-detail'),
    path('projects/stats/', views.project_stats_view, name='project-stats'),
    
    # Protected endpoints (require authentication and project access)
    path('projects/<int:project_id>/financial/', views.project_financial_info, name='project-financial'),
    path('projects/<int:project_id>/simulator-config/', views.project_simulator_config, name='project-simulator-config'),
    
    # Admin endpoints (for future dashboard)
    path('admin/projects/', views.SolarProjectCreateView.as_view(), name='project-create'),
    path('admin/projects/<int:pk>/', views.SolarProjectUpdateView.as_view(), name='project-update'),
    path('admin/projects/<int:pk>/delete/', views.SolarProjectDeleteView.as_view(), name='project-delete'),
]