#!/usr/bin/env python
"""
Script para actualizar el tipo de cambio USD/ARS
Uso: python update_exchange_rate.py
"""

import os
import sys
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesolar.settings')
django.setup()

from simulations.models import ExchangeRate


def update_exchange_rate(new_rate: float, source: str = "Manual"):
    """
    Actualiza el tipo de cambio en la base de datos
    
    Args:
        new_rate: Nuevo tipo de cambio ARS/USD
        source: Fuente del tipo de cambio (default: "Manual")
    """
    try:
        # Crear nuevo tipo de cambio
        nuevo_tdc = ExchangeRate.objects.create(
            rate=new_rate,
            source=source,
            date=date.today()
        )
        
        print(f"✅ Tipo de cambio actualizado exitosamente:")
        print(f"   Valor: ${nuevo_tdc.rate} ARS/USD")
        print(f"   Fecha: {nuevo_tdc.date}")
        print(f"   Fuente: {nuevo_tdc.source}")
        
        # Verificar que es el más reciente
        ultimo_tdc = ExchangeRate.get_latest_rate()
        print(f"\n🔄 TDC actual del sistema: ${ultimo_tdc} ARS/USD")
        
        # Mostrar últimos 5 tipos de cambio
        print(f"\n📊 Últimos tipos de cambio:")
        for rate in ExchangeRate.objects.all()[:5]:
            print(f"   {rate.date}: ${rate.rate} ARS/USD ({rate.source})")
            
        return nuevo_tdc
        
    except Exception as e:
        print(f"❌ Error al actualizar tipo de cambio: {e}")
        return None


if __name__ == "__main__":
    print("🔄 Actualizando tipo de cambio a $1330 ARS/USD...")
    print("-" * 50)
    
    # Actualizar a 1330 ARS/USD
    resultado = update_exchange_rate(1330.00, "Actualización manual")
    
    if resultado:
        print(f"\n✅ Proceso completado exitosamente")
        print(f"   El sistema ahora usará ${resultado.rate} ARS/USD para nuevas simulaciones")
    else:
        print(f"\n❌ Error en el proceso")
        sys.exit(1)

