#!/usr/bin/env python
"""
Script para configuración inicial de WeSolar
Crea datos de ejemplo para desarrollo y testing
"""

import os
import django
import sys
from decimal import Decimal
from datetime import date, timedelta

# Configure Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesolar.settings')
django.setup()

from projects.models import SolarProject, ProjectImage
from simulations.models import TariffCategory, ExchangeRate
from core.models import SiteSettings


def create_tariff_categories():
    """Create simplified tariff categories"""
    print("Creating tariff categories...")
    
    categories = [
        {
            'name': 'Residencial',
            'code': 'RES',
            'description': 'Categoría para usuarios residenciales',
        },
        {
            'name': 'Comercial',
            'code': 'COM',
            'description': 'Categoría para establecimientos comerciales',
        },
        {
            'name': 'Industrial',
            'code': 'IND',
            'description': 'Categoría para instalaciones industriales',
        },
        {
            'name': 'Grandes Consumos',
            'code': 'GC',
            'description': 'Categoría para grandes consumidores de energía',
        },
    ]
    
    for cat_data in categories:
        category, created = TariffCategory.objects.get_or_create(
            code=cat_data['code'],
            defaults=cat_data
        )
        if created:
            print(f"  ✓ Created: {category.name}")
        else:
            print(f"  - Exists: {category.name}")


def create_exchange_rates():
    """Create sample exchange rates only if none exist"""
    print("Creating exchange rates...")
    
    # Check if exchange rates already exist
    existing_count = ExchangeRate.objects.count()
    if existing_count > 0:
        print(f"  ⚠️  Exchange rates already exist ({existing_count} records)")
        print("  → Skipping creation to preserve existing rates")
        return
    
    # Create rates for the last 30 days using current blue dollar rate
    base_rate = Decimal('1330.00')  # Updated to blue dollar rate
    today = date.today()
    
    for i in range(30):
        rate_date = today - timedelta(days=i)
        # Add some variation to the rate (±10 ARS)
        variation = (i % 7) - 3  # -3 to +3
        rate = base_rate + Decimal(str(variation * 3))  # ±9 ARS variation
        
        exchange_rate, created = ExchangeRate.objects.get_or_create(
            date=rate_date,
            source='Manual',
            defaults={'rate': rate}
        )
        
        if created and i < 5:  # Only print first 5
            print(f"  ✓ Created rate for {rate_date}: ${rate} ARS/USD")


def create_solar_projects():
    """Create sample solar projects"""
    print("Creating solar projects...")
    
    projects = [
        {
            'name': 'Cooperativa Ganadera, Agrícola y de consumo Porteña LTDA.',
            'description': 'Instalación solar de 396 kWp ubicada en Porteña, Córdoba. La instalación consta de 600 módulos fotovoltaicos de marca Trina Solar modelo TSM-660DE21, con tecnología bifacial. Cada panel posee una potencia nominal de aproximadamente 660 Wp. Se emplean tres inversores Sungrow SG110CX-P2, del tipo string trifásico con una potencia nominal de 110 kW cada uno, que permiten una eficiente conversión de energía DC a AC para inyección a red. Esta marca de inversores, líder a nivel mundial, ofrece comunicación y monitoreo de la planta solar a través de una plataforma en línea llamada iSolarCloud.',
            'location': 'Porteña, Córdoba, Argentina',
            'status': 'operational',
            'total_power_installed': Decimal('396.00'),
            'total_power_projected': Decimal('396.00'),
            'available_power': Decimal('396.00'),
            'price_per_wp_usd': Decimal('1.20'),
            'price_per_panel_usd': Decimal('792.00'),
            'panel_power_wp': Decimal('660'),
            'owners': 'Cooperativa Ganadera, Agrícola y de consumo Porteña LTDA.',
            'expected_annual_generation': Decimal('631350'),
            'funding_goal': Decimal('475200'),
            'funding_raised': Decimal('0.00'),
            'funding_deadline': date.today() - timedelta(days=365),
            'commercial_whatsapp': '+54 9 351 703-5589',
        },
        {
            'name': 'Cooperativa Luz y Fuerza Villa General Belgrano',
            'description': 'Parque solar de 1 MW ubicado en Villa General Belgrano, Córdoba. La instalación cuenta con aproximadamente 1,515 módulos fotovoltaicos de marca Trina Solar modelo TSM-660DE21, con tecnología bifacial. Cada panel posee una potencia nominal de 660 Wp, totalizando una potencia instalada de 1 MW. Este proyecto de la Cooperativa Luz y Fuerza representa un hito en el desarrollo de energías renovables en la región, contribuyendo significativamente al suministro de energía limpia y sostenible.',
            'location': 'Villa General Belgrano, Córdoba, Argentina',
            'status': 'development',
            'total_power_installed': Decimal('0.00'),
            'total_power_projected': Decimal('1000.00'),
            'available_power': Decimal('1000.00'),
            'price_per_wp_usd': Decimal('1.20'),
            'price_per_panel_usd': Decimal('792.00'),
            'panel_power_wp': Decimal('660'),
            'owners': 'Cooperativa Luz y Fuerza Villa General Belgrano',
            'expected_annual_generation': Decimal('1500000'),
            'funding_goal': Decimal('1200000'),
            'funding_raised': Decimal('0.00'),
            'funding_deadline': date.today() + timedelta(days=45),
            'financial_access_password': 'iris2025',
            'commercial_whatsapp': '+54 9 351 703-5589',
        },
    ]
    
    for proj_data in projects:
        project, created = SolarProject.objects.get_or_create(
            name=proj_data['name'],
            defaults=proj_data
        )
        if created:
            print(f"  ✓ Created: {project.name}")
        else:
            print(f"  - Exists: {project.name}")


def create_project_images():
    """Create project images"""
    print("Creating project images...")
    
    project_images = [
        {
            'project_name': 'Cooperativa Ganadera, Agrícola y de consumo Porteña LTDA.',
            'image_path': 'projects/cooperativa-portena-solar.jpg',
            'caption': 'Instalación solar de la Cooperativa Ganadera en Porteña, Córdoba',
            'is_featured': True,
            'order': 1
        },
        {
            'project_name': 'Cooperativa Luz y Fuerza Villa General Belgrano',
            'image_path': 'projects/vgb.jpg',
            'caption': 'Instalación solar de la Cooperativa Luz y Fuerza en Villa General Belgrano, Córdoba',
            'is_featured': True,
            'order': 1
        },
    ]
    
    for img_data in project_images:
        try:
            project = SolarProject.objects.get(name=img_data['project_name'])
            image, created = ProjectImage.objects.get_or_create(
                project=project,
                image=img_data['image_path'],
                defaults={
                    'caption': img_data['caption'],
                    'is_featured': img_data['is_featured'],
                    'order': img_data['order']
                }
            )
            if created:
                print(f"  ✓ Created image for: {project.name}")
            else:
                print(f"  - Image exists for: {project.name}")
        except SolarProject.DoesNotExist:
            print(f"  ❌ Project not found: {img_data['project_name']}")


def create_site_settings():
    """Create site settings"""
    print("Creating site settings...")
    
    settings_data = {
        'site_name': 'Simulador CS',
        'site_description': 'Plataforma líder en simulación y cotización de inversiones en Comunidades Solares. Simulamos tus escenarios de inversión en energía solar.',
        'contact_email': 'info@simuladorcs.com',
        'contact_phone': '54 11 4000-5000',
        'address': 'Av. Menéndez Pidal 3857, Córdoba, Argentina',
        'facebook_url': 'https://facebook.com/simuladorcs',
        'twitter_url': 'https://twitter.com/simuladorcs',
        'linkedin_url': 'https://linkedin.com/company/simuladorcs',
        'instagram_url': 'https://instagram.com/simuladorcs',
        'meta_keywords': 'energía solar, inversión, renovables, sustentabilidad, paneles solares, argentina',
        'default_annual_generation_factor': Decimal('1500.00'),
        'default_performance_ratio': Decimal('0.850'),
    }
    
    settings, created = SiteSettings.objects.get_or_create(
        pk=1,
        defaults=settings_data
    )
    
    if created:
        print(f"  ✓ Created site settings")
    else:
        print(f"  - Updated site settings")
        for key, value in settings_data.items():
            setattr(settings, key, value)
        settings.save()


def main():
    """Run the initial setup"""
    print("🚀 Iniciando configuración inicial de WeSolar...\n")
    
    try:
        create_site_settings()
        print()
        
        create_tariff_categories()
        print()
        
        create_exchange_rates()
        print()
        
        create_solar_projects()
        print()
        
        create_project_images()
        print()
        
        print("✅ Configuración inicial completada exitosamente!")
        print("\n📋 Resumen:")
        print(f"   • Proyectos solares: {SolarProject.objects.count()}")
        print(f"   • Imágenes de proyectos: {ProjectImage.objects.count()}")
        print(f"   • Categorías tarifarias: {TariffCategory.objects.count()}")
        print(f"   • Tipos de cambio: {ExchangeRate.objects.count()}")
        print(f"   • Configuración del sitio: ✓")
        
        print("\n🔧 Próximos pasos:")
        print("   1. Ejecutar el servidor: python manage.py runserver")
        print("   2. Crear superusuario: python manage.py createsuperuser")
        print("   3. Acceder al admin: http://localhost:8000/admin/")
        print("   4. Ver la API: http://localhost:8000/api/docs/")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)