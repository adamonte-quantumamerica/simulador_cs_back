@echo off
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [INFO] Ejecutando migraciones...
python manage.py makemigrations
python manage.py migrate

echo [INFO] Cargando datos iniciales...
python initial_setup.py

echo [INFO] Iniciando servidor Django...
python manage.py runserver

pause