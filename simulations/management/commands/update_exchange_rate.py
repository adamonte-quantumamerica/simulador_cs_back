"""
Django management command to update exchange rate to blue dollar
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import date
from simulations.models import ExchangeRate


class Command(BaseCommand):
    help = 'Update exchange rate to current blue dollar rate (1330 ARS/USD)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--rate',
            type=float,
            default=1330.0,
            help='Exchange rate to set (default: 1330 ARS/USD)'
        )

    def handle(self, *args, **options):
        blue_rate = Decimal(str(options['rate']))
        today = date.today()
        
        self.stdout.write("=== ACTUALIZANDO TIPO DE CAMBIO ===\n")
        
        # Crear o actualizar el tipo de cambio de hoy
        exchange_rate, created = ExchangeRate.objects.get_or_create(
            date=today,
            source='Dólar Blue',
            defaults={'rate': blue_rate}
        )
        
        if not created:
            # Si ya existe, actualizar el valor
            old_rate = exchange_rate.rate
            exchange_rate.rate = blue_rate
            exchange_rate.source = 'Dólar Blue'
            exchange_rate.save()
            self.stdout.write(f"✅ ACTUALIZADO: {today}")
            self.stdout.write(f"   Anterior: ${old_rate} ARS/USD")
            self.stdout.write(f"   Nuevo: ${blue_rate} ARS/USD")
        else:
            self.stdout.write(f"✅ CREADO: {today}")
            self.stdout.write(f"   Tipo de cambio: ${blue_rate} ARS/USD")
            self.stdout.write(f"   Fuente: Dólar Blue")
        
        # Verificar que es el más reciente
        current_rate = ExchangeRate.get_latest_rate()
        self.stdout.write(f"\n🔄 Tipo de cambio activo: ${current_rate} ARS/USD")
        
        # Mostrar impacto en cálculo de ejemplo
        panels = 12
        investment_usd = 6000  # 12 paneles × $500
        investment_ars = investment_usd * current_rate
        
        self.stdout.write(f"\n💰 IMPACTO EN CÁLCULOS:")
        self.stdout.write(f"   Ejemplo (12 paneles):")
        self.stdout.write(f"   • Inversión USD: ${investment_usd:,}")
        self.stdout.write(f"   • Inversión ARS: ${investment_ars:,.0f}")
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Tipo de cambio actualizado exitosamente!')
        )
