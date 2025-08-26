# Restricciones Basadas en Factura para Simulaciones

## 📋 Resumen

Se han implementado restricciones inteligentes en todas las simulaciones para evitar inversiones excesivas o poco razonables basadas en el monto de la factura mensual del usuario.

## 🎯 Objetivo

Prevenir que los usuarios inviertan más dinero del que pueden recuperar a través de los ahorros en su factura eléctrica, garantizando períodos de retorno razonables.

## 🔢 Lógica de Restricciones

### Cálculo de Límites Máximos

```python
def _calculate_bill_based_limits(self, monthly_bill_ars: Decimal) -> Dict[str, Any]:
    # Período de retorno máximo: 10 años
    max_payback_years = 10
    max_total_savings = monthly_bill_ars * 12 * max_payback_years
    
    # Inversión máxima = 10 años de facturas
    max_investment_ars = max_total_savings
    max_investment_usd = max_investment_ars / exchange_rate
    
    # Paneles máximos para 100% de cobertura
    ahorro_por_panel = 0.66 × 101.25 × 24 × 30 × 0.19 = 9,142 ARS/mes
    max_panels_for_bill = monthly_bill_ars / ahorro_por_panel
    
    return limits
```

### Aplicación de Restricciones

#### 1. **Simulación por Número de Paneles**
```python
# Máximo permitido: exactamente lo necesario para 100% cobertura (factura = ahorro)
max_panels = max_panels_for_bill_coverage
restricted_panels = min(requested_panels, max_panels)
```

#### 2. **Simulación por Inversión**
```python
# Inversión no puede exceder lo necesario para 100% cobertura
max_panels_100_coverage = monthly_bill / ahorro_por_panel
max_investment = calculate_total_investment_tiered(max_panels_100_coverage)
restricted_investment = min(requested_investment, max_investment)
```

#### 3. **Simulación por Cobertura**
- No aplica restricciones directas (es inherentemente limitada por el % solicitado)
- Pero el cálculo respeta los límites físicos de generación

## 📊 Ejemplos de Aplicación

### Caso 1: Factura Baja - Solicitud Excesiva
- **Factura**: $50,000 ARS/mes
- **Solicitud**: 100 paneles
- **Restricción**: Máximo 5 paneles (95 paneles reducidos)
- **Justificación**: 5 paneles = 91.4% cobertura (máximo razonable)

### Caso 2: Factura Media - Solicitud Razonable  
- **Factura**: $200,000 ARS/mes
- **Solicitud**: 25 paneles
- **Restricción**: Máximo 22 paneles (3 paneles reducidos)
- **Cobertura resultante**: 100.6% (100% cobertura exacta)

### Caso 3: Factura Alta - Dentro de Límites
- **Factura**: $500,000 ARS/mes  
- **Solicitud**: 50 paneles
- **Restricción**: Sin restricción (máximo ~55 paneles)
- **Cobertura resultante**: ~91.4% (dentro del límite de 100%)

## 🔧 Parámetros Configurables

### Límites Actuales
- **Cobertura máxima**: 100% exacto (factura = ahorro mensual)
- **Paneles máximos**: Cantidad exacta para 100% cobertura
- **Inversión máxima**: Costo de paneles para 100% cobertura
- **Base de cálculo**: Factura mensual actual

### Fórmulas de Ahorro
- **Ahorro por panel**: $9,142 ARS/mes/panel
- **Fórmula**: `0.66 × 101.25 × 24 × 30 × 0.19`

## 📈 Beneficios Implementados

### 1. **Protección al Usuario**
- Evita inversiones desproporcionadas
- Garantiza períodos de retorno razonables
- Previene exceso de capacidad instalada

### 2. **Coherencia Financiera**
- Inversión alineada con capacidad de ahorro
- ROI predecible y sostenible
- Análisis de riesgo implícito

### 3. **Experiencia Mejorada**
- Sugerencias automáticas dentro de límites razonables
- Educación implícita sobre dimensionamiento
- Prevención de expectativas irreales

## 🚨 Casos de Restricción

### Cuándo se Aplican
1. **Paneles excesivos**: Más del 150% de cobertura total
2. **Inversión desproporcionada**: Más de 10 años de facturas
3. **Períodos de retorno muy largos**: > 10 años

### Comunicación al Usuario
Las restricciones son transparentes y el sistema:
- Calcula automáticamente los límites
- Aplica la restricción sin error
- Proporciona el resultado optimizado
- (Futuro: Mensaje explicativo de por qué se limitó)

## 🔄 Integración en el Sistema

### Archivos Modificados
- ✅ `simulation_engine.py`: Nuevos métodos de restricción
- ✅ Todos los simuladores actualizados
- ✅ Cálculos integrados con precios escalonados

### Compatibilidad
- ✅ Funciona con todas las simulaciones existentes
- ✅ Mantiene la API actual
- ✅ No rompe funcionalidad anterior
- ✅ Mejora la calidad de resultados

Las restricciones operan de manera silenciosa y transparente, mejorando automáticamente la calidad de las simulaciones sin requerir cambios en el frontend.
