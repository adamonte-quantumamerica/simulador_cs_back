from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.hashers import check_password
from decimal import Decimal
from .models import InvestmentSimulation, TariffCategory, ExchangeRate
from projects.models import SolarProject
from .serializers import (
    InvestmentSimulationSerializer,
    SimulationInputSerializer,
    TariffCategorySerializer,
    ExchangeRateSerializer,
    SimulationSummarySerializer,
    SimulationComparisonSerializer
)
from .simulation_engine import SolarInvestmentCalculator
from projects.models import SolarProject


def _check_project_access(user, project, access_code=None):
    """
    Función auxiliar para verificar si un usuario tiene acceso a un proyecto
    """
    # Importar aquí para evitar imports circulares
    from authentication.models import ProjectAccess
    
    # Verificar si ya tiene acceso concedido
    if ProjectAccess.objects.filter(user=user, project=project).exists():
        return True
    
    # Verificar si proporciona un código de acceso válido
    if access_code:
        return (
            check_password(access_code, project.financial_access_password) or
            access_code == project.financial_access_password
        )
    
    return False


class TariffCategoryListView(generics.ListAPIView):
    """
    API view to list all available tariff categories
    """
    queryset = TariffCategory.objects.all()
    serializer_class = TariffCategorySerializer


class ExchangeRateListView(generics.ListAPIView):
    """
    API view to list exchange rates
    """
    queryset = ExchangeRate.objects.all()[:10]  # Latest 10 rates
    serializer_class = ExchangeRateSerializer


@api_view(['GET'])
def current_exchange_rate_view(request):
    """
    API view to get the current exchange rate
    """
    try:
        rate = ExchangeRate.get_latest_rate()
        return Response({
            'current_rate': float(rate),
            'currency_pair': 'USD/ARS'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Error al obtener el tipo de cambio'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def calculate_limits_view(request):
    """
    API view to calculate maximum investment and panels based on monthly bill
    """
    try:
        monthly_bill_ars = request.data.get('monthly_bill_ars')
        project_id = request.data.get('project_id')
        tariff_category_id = request.data.get('tariff_category_id')
        
        if not all([monthly_bill_ars, project_id, tariff_category_id]):
            return Response(
                {'error': 'monthly_bill_ars, project_id y tariff_category_id son requeridos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate and get objects
        try:
            monthly_bill_ars = Decimal(str(monthly_bill_ars))
            if monthly_bill_ars <= 0:
                raise ValueError("monthly_bill_ars debe ser mayor a 0")
        except (ValueError, TypeError) as e:
            return Response(
                {'error': 'monthly_bill_ars debe ser un número válido mayor a 0'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            project = SolarProject.objects.get(id=project_id)
            tariff_category = TariffCategory.objects.get(id=tariff_category_id)
        except (SolarProject.DoesNotExist, TariffCategory.DoesNotExist):
            return Response(
                {'error': 'Proyecto o categoría tarifaria no encontrados'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Initialize calculator and calculate limits
        from .simulation_engine import SolarInvestmentCalculator
        calculator = SolarInvestmentCalculator(project, tariff_category)
        limits = calculator._calculate_bill_based_limits(monthly_bill_ars)
        
        # Calculate max investment based on 100% coverage
        max_panels_100_coverage = limits['max_panels_for_bill_coverage']
        max_investment_usd_100_coverage = calculator._calculate_total_investment_tiered(max_panels_100_coverage)
        max_investment_ars_100_coverage = max_investment_usd_100_coverage * calculator.exchange_rate
        
        # Format response
        response_data = {
            'monthly_bill_ars': float(monthly_bill_ars),
            'max_investment_usd': float(max_investment_usd_100_coverage),
            'max_investment_ars': float(max_investment_ars_100_coverage),
            'max_panels_100_coverage': limits['max_panels_for_bill_coverage'],
            'max_panels_allowed': limits['max_panels_for_bill_coverage'],  # Same as 100% coverage
            'savings_per_panel_ars': float(limits['savings_per_panel_ars']),
            'max_payback_years': limits['max_payback_years'],
            'exchange_rate_used': float(calculator.exchange_rate)
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error al calcular límites: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_simulation_view(request):
    """
    API view to create a new investment simulation (requires authentication and project access)
    """
    serializer = SimulationInputSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            with transaction.atomic():
                # Get required objects
                project = get_object_or_404(SolarProject, id=serializer.validated_data['project_id'])
                tariff_category = get_object_or_404(
                    TariffCategory, 
                    id=serializer.validated_data['tariff_category_id']
                )
                
                # Verificar acceso al proyecto
                access_code = serializer.validated_data.get('access_code')
                if not _check_project_access(request.user, project, access_code):
                    return Response(
                        {'error': 'Acceso denegado. Verifique el código de acceso del proyecto.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # Si proporciona código válido, crear el acceso
                if access_code:
                    from authentication.models import ProjectAccess
                    ProjectAccess.objects.get_or_create(user=request.user, project=project)
                
                # Initialize calculator
                calculator = SolarInvestmentCalculator(project, tariff_category)
                
                # Determine simulation type and run calculation
                user_email = serializer.validated_data.get('user_email', request.user.email)
                user_phone = serializer.validated_data.get('user_phone', '')
                
                if serializer.validated_data.get('bill_coverage_percentage') is not None:
                    simulation = calculator.simulate_by_bill_coverage(
                        monthly_bill_ars=serializer.validated_data['monthly_bill_ars'],
                        bill_coverage_percentage=serializer.validated_data['bill_coverage_percentage'],
                        user_email=user_email,
                        user_phone=user_phone
                    )
                elif serializer.validated_data.get('number_of_panels') is not None:
                    simulation = calculator.simulate_by_panels(
                        monthly_bill_ars=serializer.validated_data['monthly_bill_ars'],
                        number_of_panels=serializer.validated_data['number_of_panels'],
                        user_email=user_email,
                        user_phone=user_phone
                    )
                elif serializer.validated_data.get('investment_amount_usd') is not None:
                    simulation = calculator.simulate_by_investment(
                        monthly_bill_ars=serializer.validated_data['monthly_bill_ars'],
                        investment_amount_usd=serializer.validated_data['investment_amount_usd'],
                        user_email=user_email,
                        user_phone=user_phone
                    )
                
                # Asociar la simulación con el usuario autenticado
                simulation.user = request.user
                
                # Save simulation
                simulation.save()
                
                # Check project capacity
                capacity_check = calculator.get_project_capacity_check(simulation.installed_power_kw)
                
                # Serialize response
                response_serializer = InvestmentSimulationSerializer(simulation)
                
                return Response({
                    'simulation': response_serializer.data,
                    'capacity_check': capacity_check,
                    'success': True
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': f'Error al crear la simulación: {str(e)}',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'errors': serializer.errors,
        'success': False
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def compare_simulations_view(request):
    """
    API view to compare multiple simulation scenarios
    """
    serializer = SimulationComparisonSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            # Get required objects
            project = get_object_or_404(SolarProject, id=serializer.validated_data['project_id'])
            tariff_category = get_object_or_404(
                TariffCategory, 
                id=serializer.validated_data['tariff_category_id']
            )
            
            # Initialize calculator
            calculator = SolarInvestmentCalculator(project, tariff_category)
            monthly_bill = serializer.validated_data['monthly_bill_ars']
            
            comparison_results = []
            
            # Bill coverage percentage scenarios
            if serializer.validated_data.get('bill_coverage_percentages'):
                for coverage in serializer.validated_data['bill_coverage_percentages']:
                    simulation = calculator.simulate_by_bill_coverage(monthly_bill, coverage)
                    simulation_data = InvestmentSimulationSerializer(simulation).data
                    comparison_results.append({
                        'type': 'bill_coverage',
                        'parameter': float(coverage),
                        'simulation': simulation_data
                    })
            
            # Panel quantity scenarios
            if serializer.validated_data.get('panel_quantities'):
                for panels in serializer.validated_data['panel_quantities']:
                    simulation = calculator.simulate_by_panels(monthly_bill, panels)
                    simulation_data = InvestmentSimulationSerializer(simulation).data
                    comparison_results.append({
                        'type': 'panels',
                        'parameter': panels,
                        'simulation': simulation_data
                    })
            
            # Investment amount scenarios
            if serializer.validated_data.get('investment_amounts'):
                for amount in serializer.validated_data['investment_amounts']:
                    simulation = calculator.simulate_by_investment(monthly_bill, amount)
                    simulation_data = InvestmentSimulationSerializer(simulation).data
                    comparison_results.append({
                        'type': 'investment',
                        'parameter': float(amount),
                        'simulation': simulation_data
                    })
            
            return Response({
                'project_info': {
                    'id': project.id,
                    'name': project.name,
                    'available_power_kw': float(project.available_power)
                },
                'comparison_results': comparison_results,
                'success': True
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Error al comparar simulaciones: {str(e)}',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'errors': serializer.errors,
        'success': False
    }, status=status.HTTP_400_BAD_REQUEST)


class SimulationDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific simulation by ID (only for the owner)
    """
    serializer_class = InvestmentSimulationSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Solo simulaciones del usuario autenticado
        return InvestmentSimulation.objects.filter(user=self.request.user)


class UserSimulationsView(generics.ListAPIView):
    """
    API view to list simulations for the authenticated user
    """
    serializer_class = SimulationSummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filtrar por usuario autenticado
        return InvestmentSimulation.objects.filter(user=self.request.user).select_related('project')


@api_view(['GET'])
def simulation_stats_view(request):
    """
    API view to get general simulation statistics
    """
    try:
        total_simulations = InvestmentSimulation.objects.count()
        
        # Average metrics
        if total_simulations > 0:
            from django.db.models import Avg
            avg_investment = InvestmentSimulation.objects.aggregate(
                avg=Avg('total_investment_usd')
            )['avg'] or 0
            
            avg_payback = InvestmentSimulation.objects.aggregate(
                avg=Avg('payback_period_years')
            )['avg'] or 0
            
            avg_roi = InvestmentSimulation.objects.aggregate(
                avg=Avg('roi_annual')
            )['avg'] or 0
        else:
            avg_investment = avg_payback = avg_roi = 0
        
        stats = {
            'total_simulations': total_simulations,
            'average_investment_usd': float(avg_investment),
            'average_payback_years': float(avg_payback),
            'average_roi_annual': float(avg_roi),
        }
        
        return Response(stats, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': 'Error al obtener estadísticas'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )