#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesolar.settings')
django.setup()

from projects.models import SolarProject

print("=== VERIFICANDO DATOS DEL PROYECTO ===")

project = SolarProject.objects.get(id=10)  # El ID del proyecto de tu log
print(f"Proyecto: {project.name}")
print(f"Potencia disponible: {project.available_power} kWp")
print(f"Potencia por panel: {project.panel_power_wp} Wp")

# Calcular máximo de paneles basado en capacidad del proyecto
panel_power_kw = float(project.panel_power_wp) / 1000
max_panels_by_capacity = int(float(project.available_power) / panel_power_kw)

print(f"\n=== CÁLCULO CAPACIDAD PROYECTO ===")
print(f"Panel power: {panel_power_kw} kW")
print(f"Max paneles por capacidad: {max_panels_by_capacity}")

print(f"\n¿Es este el valor que aparece como 500?")
if max_panels_by_capacity == 500:
    print("✅ SÍ - Este es el problema!")
    print("El proyecto tiene capacidad para 500 paneles, y ese límite está sobrescribiendo el límite de factura (5 paneles)")
else:
    print(f"❌ NO - Expected 500 but got {max_panels_by_capacity}")
