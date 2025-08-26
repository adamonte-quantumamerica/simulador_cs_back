"""
Django management command to clean and set the correct exchange rate
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import date
from simulations.models import ExchangeRate


class Command(BaseCommand):
    help = 'Clean old exchange rates and set blue dollar rate as the only active rate'

    def handle(self, *args, **options):
        blue_rate = Decimal('1330.00')
        today = date.today()
        
        self.stdout.write("=== LIMPIANDO Y CONFIGURANDO TIPO DE CAMBIO ===\n")
        
        # Eliminar todos los tipos de cambio existentes
        old_count = ExchangeRate.objects.count()
        ExchangeRate.objects.all().delete()
        self.stdout.write(f"🗑️  Eliminados {old_count} tipos de cambio anteriores")
        
        # Crear el nuevo tipo de cambio del dólar blue
        exchange_rate = ExchangeRate.objects.create(
            date=today,
            source='Dólar Blue',
            rate=blue_rate
        )
        
        self.stdout.write(f"✅ CREADO: {today}")
        self.stdout.write(f"   Tipo de cambio: ${blue_rate} ARS/USD")
        self.stdout.write(f"   Fuente: Dólar Blue")
        
        # Verificar que es el activo
        current_rate = ExchangeRate.get_latest_rate()
        self.stdout.write(f"\n🔄 Tipo de cambio activo: ${current_rate} ARS/USD")
        
        # Mostrar impacto en cálculos
        panels = 12
        investment_usd = 6000  # 12 paneles × $500
        investment_ars = investment_usd * current_rate
        
        self.stdout.write(f"\n💰 IMPACTO EN CÁLCULOS:")
        self.stdout.write(f"   Ejemplo (12 paneles):")
        self.stdout.write(f"   • Inversión USD: ${investment_usd:,}")
        self.stdout.write(f"   • Inversión ARS: ${investment_ars:,.0f}")
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Tipo de cambio configurado exitosamente!')
        )
