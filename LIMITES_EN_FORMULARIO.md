# Visualización de Límites en el Formulario de Simulación

## 📋 Resumen

Se ha implementado la visualización de límites máximos recomendados directamente en el formulario de simulación, proporcionando transparencia y orientación al usuario sobre los rangos razonables de inversión y cantidad de paneles.

## 🎯 Objetivo

Mostrar al usuario en tiempo real cuáles son los límites máximos recomendados basados en su factura mensual, educándolo sobre inversiones responsables y períodos de retorno razonables.

## 🔧 Implementación Técnica

### Backend: Nuevo Endpoint API

#### Endpoint
```
POST /api/v1/calculate-limits/
```

#### Parámetros de Entrada
```json
{
  "monthly_bill_ars": 100000,
  "project_id": 1,
  "tariff_category_id": 1
}
```

#### Respuesta
```json
{
  "monthly_bill_ars": 100000.0,
  "max_investment_usd": 9023.0,
  "max_investment_ars": 12000000.0,
  "max_panels_100_coverage": 11,
  "max_panels_allowed": 16,
  "savings_per_panel_ars": 9142.0,
  "max_payback_years": 10,
  "exchange_rate_used": 1330.0
}
```

#### Validaciones
- `monthly_bill_ars` debe ser > 0
- `project_id` debe existir
- `tariff_category_id` debe existir

### Frontend: Visualización Inteligente

#### Activación Automática
La información de límites se calcula y muestra automáticamente cuando:
1. El usuario ingresa una factura mensual válida
2. Está seleccionado un proyecto
3. Está seleccionada una categoría tarifaria

#### Estados de Visualización

**1. Calculando**
```jsx
{limitsLoading && (
  <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
    <div className="flex items-center space-x-2 text-sm text-gray-500">
      <LoadingSpinner size="small" />
      <span>Calculando límites...</span>
    </div>
  </div>
)}
```

**2. Límites Disponibles**
```jsx
{limits && (
  <div className="bg-gradient-to-r from-blue-50 to-green-50 border border-blue-200 rounded-lg p-4">
    <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
      <HiOutlineInformationCircle className="w-5 h-5 mr-2 text-blue-500" />
      Límites Recomendados
    </h4>
    {/* Grid con información de límites */}
  </div>
)}
```

**3. Sin Datos**
- No se muestra nada si faltan parámetros requeridos

## 📊 Información Mostrada

### Límites de Inversión
- **Inversión máxima en USD**: Límite recomendado en dólares
- **Inversión máxima en ARS**: Conversión a pesos argentinos

### Límites de Paneles
- **Paneles máximos permitidos**: 150% de cobertura total (incluye margen)
- **Paneles para 100% cobertura**: Cantidad exacta para cubrir toda la factura

### Información Adicional
- **Período máximo de retorno**: 10 años
- **Ahorro por panel**: Cantidad mensual generada por cada panel

## 💡 Lógica de Cálculo

### Inversión Máxima
```
Max Inversión = Factura mensual × 12 meses × 10 años ÷ Tipo de cambio
```

### Paneles Máximos
```
Max Paneles (100%) = Factura mensual ÷ Ahorro por panel
Max Paneles (Permitidos) = Max Paneles (100%) × 1.5
```

### Validación Automática
- Los límites se recalculan al cambiar:
  - Factura mensual
  - Proyecto seleccionado  
  - Categoría tarifaria

## 🎨 Diseño Visual

### Esquema de Colores
- **Fondo**: Gradiente azul-verde suave
- **Borde**: Azul claro
- **Valores importantes**: Verde oscuro (límites máximos)
- **Valores informativos**: Gris oscuro
- **Texto adicional**: Gris medio

### Layout Responsivo
- **Desktop**: Grid de 2 columnas
- **Mobile**: Columna única
- **Elementos**: Alineación justified para valores

### Iconografía
- **Icono principal**: `HiOutlineInformationCircle` (información)
- **Loading**: Spinner animado

## 📱 Experiencia de Usuario

### Flujo de Interacción
1. **Usuario ingresa factura** → Aparece spinner "Calculando límites..."
2. **Cálculo completado** → Se muestra panel con límites
3. **Usuario modifica parámetros** → Recálculo automático
4. **Datos insuficientes** → Panel desaparece

### Beneficios para el Usuario
- **Transparencia**: Ve los límites antes de simular
- **Educación**: Comprende qué es razonable para su factura
- **Prevención**: Evita configurar simulaciones poco realistas
- **Confianza**: Entiende la base de los cálculos

## 🔄 Integración con Restricciones

### Coherencia del Sistema
Los límites mostrados en el frontend corresponden exactamente a las restricciones aplicadas en el backend:

- **Frontend**: Muestra `max_panels_allowed = 16`
- **Backend**: Limita automáticamente a máximo 16 paneles
- **Resultado**: Experiencia coherente sin sorpresas

### Flujo Completo
1. **Visualización** → Usuario ve límites en formulario
2. **Simulación** → Backend aplica automáticamente las restricciones
3. **Resultado** → Siempre dentro de parámetros mostrados

## 📁 Archivos Modificados

### Backend
- ✅ `simulations/views.py`: Nuevo endpoint `calculate_limits_view`
- ✅ `simulations/urls.py`: Nueva ruta `/calculate-limits/`

### Frontend  
- ✅ `services/api.js`: Nueva función `calculateLimits()`
- ✅ `pages/SimulationPage.js`: Estados, efectos y componente visual

## 🚀 Resultado Final

El usuario ahora ve en tiempo real:
- **"Inversión máxima: $9,023 USD"**
- **"Paneles máximos: 16 paneles"**
- **"Para 100% cobertura: 11 paneles"**
- **"Ahorro por panel: $9,142 ARS/mes"**

Esta información le permite tomar decisiones informadas antes de realizar la simulación, mejorando significativamente la experiencia y la calidad de los resultados obtenidos.
