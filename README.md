# Simulador CS - Backend

API backend para la plataforma de simulación de inversiones en energía solar comunitaria.

# Mods para Vercel

Mod 1 - rama staticfilesmanejo
Mod 2 - rama djangofilters
Mod 3 - rama favicon
Mod 4 - rama urlsfix
Mod 5 - rama djangosettingsfix
Mod 6 - rama pathimagenesfix
Mod 7 - rama manejoimagenes backend
Mod 8 - rama manejo imagenes segundo intento
Mod 9 - rama cambio de static manejo img
mod 10 - ramita imagenes
mod 11- imagenesdef

## 🚀 Tecnologías

- **Django 4.2**: Framework web
- **Django REST Framework**: API REST
- **PostgreSQL**: Base de datos (producción)
- **SQLite**: Base de datos (desarrollo)

## 📁 Estructura del Proyecto

```
simulador_cs_back/
├── authentication/         # Sistema de autenticación
├── core/                   # Funcionalidades centrales
├── projects/              # Gestión de proyectos solares
├── simulations/           # Motor de simulación
├── wesolar/              # Configuración principal
├── requirements.txt      # Dependencias
├── vercel.json          # Configuración de Vercel
└── manage.py           # CLI de Django
```

## 🔧 Instalación Local

1. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno** (crear `.env`):
```
SECRET_KEY=tu-clave-secreta
DEBUG=True
DEVELOPMENT=True
DATABASE_URL=sqlite:///db.sqlite3
```

4. **Aplicar migraciones**:
```bash
python manage.py migrate
```

5. **Crear superusuario** (opcional):
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor**:
```bash
python manage.py runserver
```

## 🌐 Deploy en Vercel

### Prerrequisitos
- Cuenta en [Vercel](https://vercel.com)
- Base de datos PostgreSQL (recomendado: [Neon](https://neon.tech))

### Variables de Entorno en Vercel
Configurar las siguientes variables en el dashboard de Vercel:

```
SECRET_KEY=clave-secreta-para-produccion
DATABASE_URL=postgresql://usuario:password@host:5432/db
DEBUG=False
DEVELOPMENT=False
```

### Pasos para Deploy

1. **Conectar repositorio a Vercel**:
   - Fork este repositorio
   - Conecta tu cuenta de GitHub a Vercel
   - Importa el repositorio en Vercel

2. **Configurar variables de entorno**:
   - Ve a tu proyecto en Vercel
   - Settings → Environment Variables
   - Agrega todas las variables necesarias

3. **Deploy automático**:
   - Cada push a `main` desplegará automáticamente
   - O deploy manual desde el dashboard

## 📊 API Endpoints

### Proyectos
- `GET /api/v1/projects/` - Listar proyectos
- `GET /api/v1/projects/{id}/` - Detalle de proyecto

### Simulaciones
- `POST /api/v1/simulations/create/` - Crear simulación
- `GET /api/v1/simulations/{id}/` - Detalle de simulación

### Core
- `POST /api/v1/contact/` - Contacto
- `GET /api/v1/settings/` - Configuración

## ⚙️ Configuración

### Base de Datos
- **Desarrollo**: SQLite automático
- **Producción**: PostgreSQL via `DATABASE_URL`

### CORS
- Configurado para dominios de frontend
- Actualizar `CORS_ALLOWED_ORIGINS` según necesidad

### Archivos Estáticos
- Servidos por Vercel en producción
- `collectstatic` automático en build

## 🔒 Seguridad

- Variables de entorno para credenciales
- CORS configurado
- Validación de entrada en API
- Rate limiting (configurar según necesidad)

## 📝 Desarrollo

### Comandos Útiles
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell interactivo
python manage.py shell

# Tests
python manage.py test
```

### Estructura de Datos
Ver modelos en cada aplicación:
- `projects/models.py` - Proyectos solares
- `simulations/models.py` - Simulaciones
- `core/models.py` - Configuración

## 📞 Soporte

Para reportar problemas o solicitar funcionalidades, crear un issue en GitHub.
