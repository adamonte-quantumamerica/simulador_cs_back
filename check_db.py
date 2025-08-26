import os
import django
from pathlib import Path
from decouple import config

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wesolar.settings')
django.setup()

from django.conf import settings
from django.db import connection

print("=" * 50)
print("CONFIGURACIÓN DE BASE DE DATOS")
print("=" * 50)

db_config = settings.DATABASES['default']
print(f"ENGINE: {db_config.get('ENGINE', 'No configurado')}")
print(f"NAME: {db_config.get('NAME', 'No configurado')}")
print(f"HOST: {db_config.get('HOST', 'No configurado')}")
print(f"PORT: {db_config.get('PORT', 'No configurado')}")
print(f"USER: {db_config.get('USER', 'No configurado')}")

print("\n" + "=" * 50)
print("VARIABLES DE ENTORNO")
print("=" * 50)
print(f"DATABASE_URL desde .env: {config('DATABASE_URL', default='No configurada')}")
print(f"DATABASE_URL desde os.getenv: {os.getenv('DATABASE_URL', 'No configurada')}")

print("\n" + "=" * 50)
print("CONEXIÓN ACTUAL")
print("=" * 50)
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        if version:
            print(f"Conectado a: {version[0]}")
        else:
            print("Conectado a SQLite (sin información de versión)")
except Exception as e:
    print(f"Error al conectar: {e}")

print("=" * 50)
