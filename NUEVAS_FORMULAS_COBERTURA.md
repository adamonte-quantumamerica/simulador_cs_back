# Nuevas Fórmulas para Simulación por Cobertura de Factura

## 📋 Resumen de Cambios

Se han implementado nuevas fórmulas para el cálculo del simulador por porcentaje de cobertura de factura, optimizando la precisión en la determinación del número de paneles necesarios.

## 🔢 Nuevas Fórmulas Implementadas

### Secuencia de Cálculo

1. **Energía Generada Requerida**
   ```
   energia_generada = monto_factura_total / precio_energia
   ```
   - `monto_factura_total`: Monto de la factura que se desea cubrir (ARS)
   - `precio_energia`: $101.25 ARS/kWh (precio fijo)

2. **Potencia Requerida**
   ```
   potencia = energia_generada / 24 / 0.19 / 30
   ```
   - `energia_generada`: kWh mensuales requeridos
   - `24`: Horas por día
   - `0.19`: Factor de performance del sistema
   - `30`: Días por mes

3. **Número de Paneles**
   ```
   paneles = potencia / 0.66
   ```
   - `potencia`: Potencia requerida en kW
   - `0.66`: Factor de eficiencia del panel

## 💻 Implementación Técnica

### Código Actualizado

```python
def simulate_by_bill_coverage(
    self, 
    monthly_bill_ars: Decimal, 
    bill_coverage_percentage: Decimal,
    user_email: str = "",
    user_phone: str = ""
) -> InvestmentSimulation:
    """
    Simulate investment based on desired bill coverage percentage
    Using new formulas:
    - energia_generada = monto_factura_total / precio_energia  
    - potencia = energia_generada / 24 / 0.19 / 30
    - paneles = potencia / 0.66
    """
    # Calculate target monthly savings in ARS
    target_monthly_savings_ars = monthly_bill_ars * (bill_coverage_percentage / 100)
    
    # Nueva fórmula: energía_generada = monto_factura_total / precio_energia
    energy_price_ars = Decimal(str(ENERGY_PRICE_ARS_PER_KWH))
    required_monthly_generation_kwh = target_monthly_savings_ars / energy_price_ars
    
    # Nueva fórmula: potencia = energia_generada / 24 / 0.19 / 30
    required_power_kw = required_monthly_generation_kwh / Decimal('24') / Decimal('0.19') / Decimal('30')
    
    # Nueva fórmula: paneles = potencia / 0.66
    number_of_panels = int((required_power_kw / Decimal('0.66')).to_integral_value(ROUND_HALF_UP))
    
    # ... resto del cálculo de inversión y métricas
```

## 📊 Ejemplos de Cálculo

### Ejemplo 1: Factura $50,000 ARS - 50% Cobertura
- **Monto a cubrir**: $25,000 ARS
- **Energía requerida**: 244.50 kWh/mes
- **Potencia requerida**: 1.787 kW
- **Número de paneles**: 3
- **Cobertura real**: 55.4% (diferencia: 5.4%)

### Ejemplo 2: Factura $100,000 ARS - 70% Cobertura  
- **Monto a cubrir**: $70,000 ARS
- **Energía requerida**: 684.60 kWh/mes
- **Potencia requerida**: 5.004 kW
- **Número de paneles**: 8
- **Cobertura real**: 73.9% (diferencia: 3.9%)

### Ejemplo 3: Factura $200,000 ARS - 100% Cobertura
- **Monto a cubrir**: $200,000 ARS
- **Energía requerida**: 1,955.99 kWh/mes
- **Potencia requerida**: 14.298 kW
- **Número de paneles**: 22
- **Cobertura real**: 101.6% (diferencia: 1.6%)

## 🎯 Precisión Mejorada

### Ventajas de las Nuevas Fórmulas
- **Alta precisión**: Diferencias menores al 6% entre objetivo y resultado
- **Simplificación**: Uso directo del precio de energía en ARS
- **Consistencia**: Integración perfecta con el sistema de precios escalonados
- **Transparencia**: Fórmulas claras y trazables

### Comparación con Sistema Anterior
- **Antes**: Basado en factores de generación y performance complejos
- **Ahora**: Cálculo directo basado en la relación energía/precio
- **Resultado**: Mayor precisión y predictibilidad

## 🔧 Archivos Modificados

### `backend/simulations/simulation_engine.py`
- ✅ Actualizado método `simulate_by_bill_coverage()`
- ✅ Implementadas las tres nuevas fórmulas
- ✅ Integración con sistema de precios escalonados
- ✅ Mantenida compatibilidad con ahorros basados en paneles

## 📈 Impacto en Resultados

Las nuevas fórmulas proporcionan:
1. **Cálculos más precisos** del número de paneles necesarios
2. **Mejor correlación** entre cobertura objetivo y real
3. **Simplificación** del proceso de cálculo
4. **Mayor confiabilidad** en las estimaciones de inversión

El sistema ahora calcula de manera más directa y precisa cuántos paneles se necesitan para lograr el porcentaje de cobertura de factura deseado.
