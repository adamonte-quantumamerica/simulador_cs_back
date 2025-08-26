from django.urls import path
from . import views

app_name = 'simulations'

urlpatterns = [
    # Tariff categories and exchange rates
    path('tariff-categories/', views.TariffCategoryListView.as_view(), name='tariff-categories'),
    path('exchange-rates/', views.ExchangeRateListView.as_view(), name='exchange-rates'),
    path('exchange-rate/current/', views.current_exchange_rate_view, name='current-exchange-rate'),
    path('calculate-limits/', views.calculate_limits_view, name='calculate-limits'),
    
    # Simulation endpoints
    path('simulations/create/', views.create_simulation_view, name='create-simulation'),
    path('simulations/compare/', views.compare_simulations_view, name='compare-simulations'),
    path('simulations/<uuid:id>/', views.SimulationDetailView.as_view(), name='simulation-detail'),
    path('simulations/user/', views.UserSimulationsView.as_view(), name='user-simulations'),
    path('simulations/stats/', views.simulation_stats_view, name='simulation-stats'),
]