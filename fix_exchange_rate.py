#!/usr/bin/env python
"""
Script para corregir el tipo de cambio y asegurar que use $1330 ARS/USD
"""

import os
import sys
import django
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesolar.settings')
django.setup()

from simulations.models import ExchangeRate


def fix_exchange_rate():
    """
    Corrige el tipo de cambio para asegurar que $1330 sea el más reciente
    """
    print("🔧 Corrigiendo tipo de cambio...")
    print("=" * 50)
    
    # Mostrar estado actual
    print("📊 Estado actual:")
    for i, rate in enumerate(ExchangeRate.objects.all()[:5], 1):
        print(f"   {i}. {rate.date}: ${rate.rate} ARS/USD ({rate.source})")
    
    # Buscar el registro de $1330
    rate_1330 = ExchangeRate.objects.filter(rate=1330.00).first()
    if not rate_1330:
        print("❌ No se encontró el TDC de $1330")
        return
    
    # Actualizar la fecha del registro de $1330 para que sea la más reciente
    today = date.today()
    rate_1330.date = today
    rate_1330.save()
    
    print(f"\n✅ TDC de $1330 actualizado con fecha {today}")
    
    # Verificar que ahora es el más reciente
    latest = ExchangeRate.get_latest_rate()
    print(f"🔄 TDC más reciente ahora: ${latest} ARS/USD")
    
    if latest == 1330.00:
        print("✅ ¡Corrección exitosa! El sistema ahora usará $1330 ARS/USD")
    else:
        print("❌ Aún hay un problema. Eliminando registros conflictivos...")
        
        # Eliminar registros que no sean de $1330 con fecha de hoy
        ExchangeRate.objects.filter(date=today).exclude(rate=1330.00).delete()
        
        latest = ExchangeRate.get_latest_rate()
        print(f"🔄 TDC final: ${latest} ARS/USD")
    
    print(f"\n📊 Estado final:")
    for i, rate in enumerate(ExchangeRate.objects.all()[:3], 1):
        print(f"   {i}. {rate.date}: ${rate.rate} ARS/USD ({rate.source})")


if __name__ == "__main__":
    fix_exchange_rate()

