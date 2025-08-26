# Sistema de Precios Escalonados por Número de Paneles

## 📋 Resumen de Cambios

Se ha implementado un nuevo sistema de precios escalonados para las simulaciones por número de paneles, reemplazando el precio fijo anterior con una estructura de descuentos por volumen que beneficia a los compradores de mayor cantidad.

## 💰 Estructura de Precios

### Tiers de Precios
- **Tier 1 (1-9 paneles)**: $700 USD por panel
- **Tier 2 (10-99 paneles)**: $500 USD por panel  
- **Tier 3 (100+ paneles)**: $400 USD por panel

### Lógica de Cálculo
El costo total se calcula aplicando un precio uniforme según el tier del número total de paneles:

```python
def _calculate_total_investment_tiered(self, number_of_panels: int) -> Decimal:
    # Determine the price per panel based on total quantity
    if number_of_panels <= 9:
        price_per_panel = Decimal('700')
    elif number_of_panels <= 99:
        price_per_panel = Decimal('500')
    else:
        price_per_panel = Decimal('400')
    
    total_cost = number_of_panels * price_per_panel
    return total_cost
```

## 📊 Ejemplos de Cálculo

### Ejemplo 1: 5 Paneles (Tier 1)
- 5 paneles × $700 = $3,500 USD
- Precio uniforme: $700/panel

### Ejemplo 2: 12 Paneles (Tier 2)
- 12 paneles × $500 = $6,000 USD
- Precio uniforme: $500/panel

### Ejemplo 3: 50 Paneles (Tier 2)
- 50 paneles × $500 = $25,000 USD
- Precio uniforme: $500/panel

### Ejemplo 4: 150 Paneles (Tier 3)
- 150 paneles × $400 = $60,000 USD
- Precio uniforme: $400/panel

## 🔄 Flujo de Cálculo Completo

### 1. Cálculo de Inversión
```python
# Usar precios escalonados
total_investment_usd = self._calculate_total_investment_tiered(number_of_panels)
total_investment_ars = total_investment_usd * self.exchange_rate
```

### 2. Especificaciones del Sistema
```python
panel_power_kw = self.project.panel_power_wp / 1000
actual_power_kw = number_of_panels * panel_power_kw
```

### 3. Generación de Energía
```python
actual_annual_generation = actual_power_kw * self.annual_generation_factor * self.performance_ratio
actual_monthly_generation = actual_annual_generation / 12
```

### 4. Cálculo de Ahorros
```python
monthly_savings_ars = self._calculate_monthly_savings(actual_monthly_generation)
annual_savings_ars = monthly_savings_ars * 12
```

### 5. Métricas Financieras
```python
# Período de retorno
payback_period = total_investment_ars / annual_savings_ars

# ROI anual
roi_annual = (annual_savings_ars / total_investment_ars) * 100

# Cobertura de factura
bill_coverage_achieved = (monthly_savings_ars / monthly_bill_ars) * 100
```

## 📈 Impacto en Resultados

### Comparación: Sistema Escalonado vs Sistema Uniforme

| Paneles | Sistema Escalonado (Anterior) | Sistema Uniforme (Actual) | Diferencia | % Cambio |
|---------|------------------------------|---------------------------|------------|----------|
| 9       | $6,300                       | $6,300                    | $0         | 0.0%     |
| 10      | $6,800                       | $5,000                    | -$1,800    | -26.5%   |
| 12      | $7,800                       | $6,000                    | -$1,800    | -23.1%   |
| 25      | $14,300                      | $12,500                   | -$1,800    | -12.6%   |
| 50      | $26,800                      | $25,000                   | -$1,800    | -6.7%    |
| 75      | $39,300                      | $37,500                   | -$1,800    | -4.6%    |
| 99      | $51,300                      | $49,500                   | -$1,800    | -3.5%    |
| 100     | $51,700                      | $40,000                   | -$11,700   | -22.6%   |
| 150     | $71,700                      | $60,000                   | -$11,700   | -16.3%   |
| 200     | $91,700                      | $80,000                   | -$11,700   | -12.8%   |

### Observaciones:
- **Proyectos 10-99 paneles**: Precio reducido significativamente (todos a $500)
- **Proyectos 100+ paneles**: Precio mucho más competitivo (todos a $400)
- **Sistema más simple**: Precio uniforme elimina complejidad de cálculo escalonado
- **Proyectos medianos (50-99 paneles)**: Incremento moderado en costo
- **Proyectos grandes (100+ paneles)**: Incremento fijo de $5,000 USD
- **Nuevo punto de equilibrio**: Aproximadamente 99-100 paneles

## 🔧 Archivos Modificados

### `backend/simulations/simulation_engine.py`
- ✅ Agregado método `_calculate_tiered_panel_price()`
- ✅ Agregado método `_calculate_total_investment_tiered()`
- ✅ Modificado método `simulate_by_panels()` para usar precios escalonados
- ✅ Actualizada documentación del método

## 🧪 Testing

### Script de Prueba: `test_tiered_pricing.py`
El script incluye:
- Creación de datos de prueba
- Pruebas con diferentes cantidades de paneles
- Desglose detallado de precios por tier
- Simulaciones completas con métricas financieras
- Comparación con sistema anterior

### Ejecutar Pruebas
```bash
cd backend
python test_tiered_pricing.py
```

## 💡 Beneficios del Sistema

### Para Compradores Pequeños
- Transparencia en precios premium
- Estructura clara y comprensible

### Para Compradores Grandes
- Descuentos automáticos por volumen
- Mejor ROI en proyectos grandes
- Incentivo para aumentar la inversión

### Para el Negocio
- Optimización de márgenes por volumen
- Incentivo a ventas de mayor escala
- Flexibilidad para ajustar tiers según mercado

## 🔮 Futuras Mejoras

1. **Tiers Configurables**: Hacer los rangos y precios configurables desde admin
2. **Precios Dinámicos**: Integrar con costos de mercado actuales
3. **Descuentos Temporales**: Sistema de promociones por tiempo limitado
4. **Personalización**: Precios especiales para clientes corporativos

## 📞 Soporte

Para consultas sobre la implementación o ajustes al sistema de precios, contactar al equipo de desarrollo.
