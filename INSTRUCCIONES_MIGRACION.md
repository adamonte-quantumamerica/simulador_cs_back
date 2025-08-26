# 🚀 Instrucciones para Actualizar el Simulador

## ⚠️ IMPORTANTE
Después de hacer `pull` de los cambios del simulador actualizado, necesitas resetear las migraciones porque se hicieron cambios estructurales importantes en la base de datos.

## 📋 Pasos para tu compañero:

### 1. Activar el entorno virtual
```bash
# En Windows
venv\Scripts\activate

# En Mac/Linux
source venv/bin/activate
```

### 2. Ejecutar el script de reseteo automático
```bash
cd backend
python reset_migrations.py
```

**¡Eso es todo!** El script hace automáticamente:
- ✅ Deshace las migraciones obsoletas
- ✅ Elimina archivos de migración antiguos  
- ✅ Crea nuevas migraciones
- ✅ Aplica las migraciones
- ✅ Ejecuta el setup inicial de datos

### 3. Verificar que funciona
```bash
python manage.py runserver
```

---

## 🔧 Si prefieres hacer los pasos manualmente:

### Opción Manual:
```bash
# 1. Activar entorno virtual
venv\Scripts\activate

# 2. Ir al directorio backend
cd backend

# 3. Deshacer migraciones de simulations
python manage.py migrate simulations zero

# 4. Eliminar archivos de migración obsoletos
# Eliminar archivos 0001_*.py, 0002_*.py, etc. en simulations/migrations/
# Eliminar carpeta simulations/migrations/__pycache__/

# 5. Crear nuevas migraciones
python manage.py makemigrations simulations --name=initial_new_structure

# 6. Aplicar migraciones
python manage.py migrate simulations
python manage.py migrate

# 7. Ejecutar setup inicial
python initial_setup.py
```

---

## 🎯 Cambios Implementados:

### Backend:
- ✅ **Campo teléfono obligatorio** con prefijo +54
- ✅ **Factura mensual en pesos** (reemplaza consumo kWh)
- ✅ **4 categorías tarifarias** simplificadas
- ✅ **Tipos de simulación actualizados** (sin prefijo "Por")
- ✅ **Precio fijo de energía** 0.06 USD/kWh

### Frontend:
- ✅ **Formularios actualizados** en ProjectDetailPage y SimulationPage
- ✅ **Validaciones nuevas** para email y teléfono
- ✅ **UI actualizada** para mostrar factura en pesos

---

## 🆘 Si hay problemas:

1. **Error de migrations**: Ejecuta `python reset_migrations.py`
2. **Error de dependencias**: Ejecuta `pip install -r requirements.txt`
3. **Error de frontend**: Ejecuta `npm install` en la carpeta frontend
4. **Base de datos corrupta**: Elimina `db.sqlite3` y ejecuta el script

---

## 📞 Contacto:
Si hay algún problema, comparte el error específico y podemos resolverlo juntos.
