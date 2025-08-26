#!/usr/bin/env python
"""
Script para resetear las migraciones después de hacer pull de los cambios estructurales.
Este script debe ejecutarse cuando se obtienen los cambios del simulador actualizado.

IMPORTANTE: Ejecutar este script reseteará todas las simulaciones existentes.
"""

import os
import django
import sys
import shutil

def setup_django():
    """Configura Django para ejecutar comandos programáticamente"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesolar.settings')
    django.setup()

def run_command(command):
    """Ejecuta un comando de Django management"""
    from django.core.management import execute_from_command_line
    print(f"\n🔧 Ejecutando: {' '.join(command)}")
    try:
        execute_from_command_line(['manage.py'] + command)
        print("✅ Comando ejecutado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def delete_migration_files():
    """Elimina archivos de migración obsoletos"""
    migrations_path = "simulations/migrations"
    if os.path.exists(migrations_path):
        for file in os.listdir(migrations_path):
            if file.startswith("000") and file.endswith(".py"):
                file_path = os.path.join(migrations_path, file)
                os.remove(file_path)
                print(f"🗑️  Eliminado: {file_path}")
        
        # Eliminar __pycache__
        pycache_path = os.path.join(migrations_path, "__pycache__")
        if os.path.exists(pycache_path):
            shutil.rmtree(pycache_path)
            print("🗑️  Eliminado: __pycache__")

def main():
    print("=" * 60)
    print("🚀 SCRIPT DE RESETEO DE MIGRACIONES - SIMULADOR ACTUALIZADO")
    print("=" * 60)
    print("\nEste script va a:")
    print("1. Deshacer todas las migraciones de 'simulations'")
    print("2. Eliminar archivos de migración obsoletos")
    print("3. Crear nuevas migraciones")
    print("4. Aplicar las nuevas migraciones")
    print("5. Ejecutar setup inicial de datos")
    print("\n⚠️  ADVERTENCIA: Esto eliminará todas las simulaciones existentes")
    
    response = input("\n¿Continuar? (s/N): ").lower().strip()
    if response != 's':
        print("❌ Operación cancelada")
        return
    
    # Configurar Django
    setup_django()
    
    print("\n📋 Paso 1: Deshaciendo migraciones de simulations...")
    if not run_command(['migrate', 'simulations', 'zero']):
        print("❌ Error deshaciendo migraciones. Continuando...")
    
    print("\n📋 Paso 2: Eliminando archivos de migración obsoletos...")
    delete_migration_files()
    
    print("\n📋 Paso 3: Creando nuevas migraciones...")
    if not run_command(['makemigrations', 'simulations', '--name=initial_new_structure']):
        print("❌ Error creando migraciones")
        return
    
    print("\n📋 Paso 4: Aplicando migraciones de simulations...")
    if not run_command(['migrate', 'simulations']):
        print("❌ Error aplicando migraciones de simulations")
        return
    
    print("\n📋 Paso 5: Aplicando todas las migraciones...")
    if not run_command(['migrate']):
        print("❌ Error aplicando todas las migraciones")
        return
    
    print("\n📋 Paso 6: Ejecutando setup inicial de datos...")
    try:
        from initial_setup import main as setup_main
        setup_main()
        print("✅ Setup inicial completado")
    except Exception as e:
        print(f"❌ Error en setup inicial: {e}")
        return
    
    print("\n" + "=" * 60)
    print("🎉 ¡RESETEO COMPLETADO EXITOSAMENTE!")
    print("=" * 60)
    print("\nEl simulador está listo con:")
    print("✅ Nuevos campos: teléfono, factura mensual")
    print("✅ Categorías tarifarias simplificadas")
    print("✅ Tipos de simulación actualizados")
    print("✅ Precio fijo de energía: 0.06 USD/kWh")
    print("\n🚀 Puedes ejecutar: python manage.py runserver")

if __name__ == "__main__":
    main()
