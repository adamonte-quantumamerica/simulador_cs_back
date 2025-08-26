# 🚀 Guía de Deployment en Vercel - WeSolar Backend

Este archivo contiene las instrucciones paso a paso para hacer el deploy del backend de WeSolar en Vercel.

## 📋 Prerequisitos

1. **Cuenta en Vercel** - Regístrate en [vercel.com](https://vercel.com)
2. **Base de datos PostgreSQL** - Configurada en Neon o similar
3. **Proyecto en GitHub** - El código debe estar en un repositorio

## 🔧 Configuración Previa

### 1. Variables de Entorno en Vercel

En el dashboard de Vercel, ve a **Settings > Environment Variables** y agrega:

```bash
# Obligatorias
SECRET_KEY=tu-clave-secreta-django-aqui
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require
DEBUG=False
DEVELOPMENT=False

# Para emails (opcional inicialmente)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion

# URLs del frontend
FRONTEND_ACTIVATION_URL=https://tu-frontend.vercel.app/activate
FRONTEND_PASSWORD_RESET_URL=https://tu-frontend.vercel.app/reset-password
```

### 2. Generar SECRET_KEY

Ejecuta en tu terminal local:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🚀 Pasos de Deployment

### 1. Conectar Repositorio
1. En Vercel, haz clic en **"New Project"**
2. Selecciona tu repositorio de GitHub
3. Vercel detectará automáticamente que es un proyecto Python

### 2. Configuración del Proyecto
- **Framework Preset**: Other
- **Root Directory**: `./` (raíz del proyecto)
- **Build Command**: `python build.py` (automático gracias a vercel.json)
- **Output Directory**: `./` (automático)

### 3. Deploy
1. Haz clic en **"Deploy"**
2. Espera a que termine el build (puede tomar 2-3 minutos)
3. Si hay errores, revisa los logs en la pestaña "Functions"

## 🔍 Verificación Post-Deploy

### 1. Verificar que la API responde
```bash
curl https://tu-app.vercel.app/api/
```

### 2. Verificar endpoints principales
```bash
# Health check
curl https://tu-app.vercel.app/api/health/

# Admin (debería redirigir al login)
curl https://tu-app.vercel.app/admin/
```

### 3. Verificar logs
- Ve a tu proyecto en Vercel Dashboard
- Pestaña **"Functions"** para ver logs de errores
- Pestaña **"Deployments"** para ver el historial

## 🛠️ Troubleshooting

### Error: "No module named 'django'"
- Verifica que `requirements.txt` esté en la raíz
- Verifica que todas las dependencias estén listadas

### Error: "ALLOWED_HOSTS"
- Agrega tu dominio de Vercel a `ALLOWED_HOSTS` en settings.py
- Ejemplo: `'tu-app.vercel.app'`

### Error: Database connection
- Verifica la variable `DATABASE_URL` en Vercel
- Asegúrate de que la base de datos acepte conexiones externas

### Error: Static files
- Los archivos estáticos se manejan automáticamente con WhiteNoise
- Si hay problemas, verifica que `whitenoise` esté en requirements.txt

## 🔒 Configuración de Seguridad

Una vez que el deploy funcione, considera agregar estas variables para mayor seguridad:

```bash
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY
```

## 📝 Archivos Creados para Vercel

- `api/index.py` - Entry point principal
- `vercel.json` - Configuración de Vercel
- `build.py` - Script de construcción
- `.vercelignore` - Archivos a ignorar
- `runtime.txt` - Versión de Python
- `env.example` - Ejemplo de variables de entorno

## 🔄 Actualizar el Deploy

Para actualizaciones futuras:
1. Haz push a tu repositorio en GitHub
2. Vercel automáticamente creará un nuevo deployment
3. Si hay problemas, puedes hacer rollback desde el dashboard

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Vercel Dashboard
2. Verifica que todas las variables de entorno estén configuradas
3. Comprueba que la base de datos esté accesible
4. Consulta la documentación oficial de Vercel

¡Tu backend de WeSolar ya debería estar funcionando en Vercel! 🎉
