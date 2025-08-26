from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import ProjectAccess


# Comentado temporalmente para usar el User por defecto
# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     """
#     Admin personalizado para el modelo User
#     """
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (_('Información Personal'), {'fields': ('first_name', 'last_name')}),
#         (_('Permisos'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Fechas Importantes'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
#     list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)
#     filter_horizontal = ('groups', 'user_permissions',)


@admin.register(ProjectAccess)
class ProjectAccessAdmin(admin.ModelAdmin):
    """
    Admin para el modelo ProjectAccess
    """
    list_display = ('user', 'project', 'granted_at')
    list_filter = ('granted_at', 'project__status')
    search_fields = ('user__email', 'project__name')
    readonly_fields = ('granted_at',)
    autocomplete_fields = ('user', 'project')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'project')