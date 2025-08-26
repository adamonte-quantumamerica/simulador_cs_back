#!/usr/bin/env python
"""
Script para verificar qué tipo de cambio se está usando para calcular el ahorro anual
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesolar.settings')
django.setup()

from simulations.models import ExchangeRate, InvestmentSimulation
from simulations.simulation_engine import SolarInvestmentCalculator
from projects.models import SolarProject


def verify_exchange_rate_usage():
    """
    Verifica qué tipo de cambio está usando el sistema para los cálculos
    """
    print("🔍 Verificando uso del tipo de cambio en cálculos...")
    print("=" * 60)
    
    # 1. Verificar TDC actual en BD
    latest_rate = ExchangeRate.get_latest_rate()
    print(f"📊 TDC más reciente en BD: ${latest_rate} ARS/USD")
    
    # Mostrar últimos 3 tipos de cambio
    print(f"\n📈 Últimos tipos de cambio registrados:")
    for i, rate in enumerate(ExchangeRate.objects.all()[:3], 1):
        print(f"   {i}. {rate.date}: ${rate.rate} ARS/USD ({rate.source})")
    
    # 2. Verificar TDC que usa el simulador
    try:
        project = SolarProject.objects.first()
        if project:
            from simulations.models import TariffCategory
            tariff = TariffCategory.objects.first()
            
            if tariff:
                calculator = SolarInvestmentCalculator(project, tariff)
                simulator_rate = calculator.exchange_rate
                print(f"\n🧮 TDC que usa el simulador: ${simulator_rate} ARS/USD")
                
                # Verificar si coinciden
                if simulator_rate == latest_rate:
                    print("✅ El simulador está usando el TDC más reciente")
                else:
                    print("⚠️  El simulador NO está usando el TDC más reciente")
                
                # 3. Ejemplo de cálculo de ahorro anual
                print(f"\n💰 Ejemplo de cálculo de ahorro anual:")
                print(f"   - Ahorro mensual: $50,000 ARS")
                print(f"   - Ahorro anual ARS: $600,000 ARS")
                print(f"   - TDC usado: ${simulator_rate} ARS/USD")
                
                monthly_savings_ars = Decimal('50000')
                annual_savings_usd = (monthly_savings_ars / simulator_rate) * 12
                print(f"   - Ahorro anual USD: ${annual_savings_usd:.2f} USD")
                
                print(f"\n📝 Fórmula usada: (ahorro_mensual_ars / tdc) * 12")
                print(f"   ({monthly_savings_ars} / {simulator_rate}) * 12 = ${annual_savings_usd:.2f} USD")
                
            else:
                print("❌ No se encontraron categorías tarifarias")
        else:
            print("❌ No se encontraron proyectos solares")
            
    except Exception as e:
        print(f"❌ Error al verificar simulador: {e}")
    
    # 4. Verificar última simulación
    print(f"\n🔬 Verificando última simulación realizada:")
    last_simulation = InvestmentSimulation.objects.first()
    if last_simulation:
        print(f"   - ID: {last_simulation.id}")
        print(f"   - TDC usado en simulación: ${last_simulation.exchange_rate_used} ARS/USD")
        print(f"   - Fecha: {last_simulation.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   - Ahorro mensual ARS: ${last_simulation.monthly_savings_ars}")
        print(f"   - Ahorro anual USD calculado: ${last_simulation.annual_savings_usd:.2f}")
        
        # Verificar si el cálculo es correcto
        expected_annual_usd = (last_simulation.monthly_savings_ars / last_simulation.exchange_rate_used) * 12
        print(f"   - Ahorro anual USD esperado: ${expected_annual_usd:.2f}")
        
        if abs(last_simulation.annual_savings_usd - expected_annual_usd) < Decimal('0.01'):
            print("   ✅ Cálculo correcto")
        else:
            print("   ⚠️  Posible error en cálculo")
    else:
        print("   No hay simulaciones registradas")


if __name__ == "__main__":
    verify_exchange_rate_usage()

