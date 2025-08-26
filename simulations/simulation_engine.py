"""
Investment Simulation Engine for Solar Projects

This module contains the core logic for calculating solar investment returns
based on user monthly bill, tariff category, and investment parameters.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, Optional
from .models import InvestmentSimulation, TariffCategory, ExchangeRate, EnergyPrice, ENERGY_PRICE_ARS_PER_KWH
from projects.models import SolarProject


class SolarInvestmentCalculator:
    """
    Calculator for solar investment simulations
    """
    
    def __init__(self, project: SolarProject, tariff_category: TariffCategory):
        self.project = project
        self.tariff_category = tariff_category
        self.exchange_rate = ExchangeRate.get_latest_rate()
        
        # Solar generation factors (typical for Argentina)
        self.annual_generation_factor = 1500  # kWh per kWp per year (average)
        self.system_degradation = Decimal('0.005')  # 0.5% annual degradation
        self.performance_ratio = Decimal('0.85')  # System efficiency
    
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
        # target_monthly_savings_ars es el equivalente al "monto de factura" que queremos cubrir
        energy_price_ars = Decimal(str(EnergyPrice.get_current_price()))
        required_monthly_generation_kwh = target_monthly_savings_ars / energy_price_ars
        
        # Nueva fórmula: potencia = energia_generada / 24 / 0.19 / 30
        required_power_kw = required_monthly_generation_kwh / Decimal('24') / Decimal('0.19') / Decimal('30')
        
        # Nueva fórmula: paneles = potencia / 0.66
        number_of_panels = int((required_power_kw / Decimal('0.66')).to_integral_value(ROUND_HALF_UP))
        
        # Recalculate actual power based on number of panels calculated
        # actual_power_kw already calculated above as required_power_kw 
        actual_power_kw = required_power_kw
        
        # Calculate actual generation based on the new formula
        actual_monthly_generation = required_monthly_generation_kwh
        actual_annual_generation = actual_monthly_generation * 12
        
        # Calculate investment using tiered pricing
        total_investment_usd = self._calculate_total_investment_tiered(number_of_panels)
        total_investment_ars = total_investment_usd * self.exchange_rate
        
        # Calculate savings using new formula (based on number of panels)
        monthly_savings_ars = self._calculate_monthly_savings(number_of_panels)
        annual_savings_ars = monthly_savings_ars * 12
        
        # Calculate annual savings in USD using blue exchange rate
        # Formula: (monthly_savings_ars / exchange_rate_blue) * 12
        annual_savings_usd = (monthly_savings_ars / self.exchange_rate) * 12
        
        # Calculate metrics
        payback_period = total_investment_ars / annual_savings_ars if annual_savings_ars > 0 else Decimal('999')
        roi_annual = (annual_savings_ars / total_investment_ars) * 100 if total_investment_ars > 0 else Decimal('0')
        actual_bill_coverage = (monthly_savings_ars / monthly_bill_ars) * 100
        
        # Create simulation object
        simulation = InvestmentSimulation(
            project=self.project,
            user_email=user_email,
            user_phone=user_phone,
            monthly_bill_ars=monthly_bill_ars,
            tariff_category=self.tariff_category,
            simulation_type='bill_coverage',
            bill_coverage_percentage=bill_coverage_percentage,
            number_of_panels=number_of_panels,
            total_investment_usd=total_investment_usd,
            total_investment_ars=total_investment_ars,
            installed_power_kw=actual_power_kw,
            annual_generation_kwh=actual_annual_generation,
            monthly_generation_kwh=actual_monthly_generation,
            monthly_savings_ars=monthly_savings_ars,
            annual_savings_ars=annual_savings_ars,
            payback_period_years=payback_period,
            bill_coverage_achieved=actual_bill_coverage,
            roi_annual=roi_annual,
            exchange_rate_used=self.exchange_rate
        )
        
        return simulation
    
    def simulate_by_panels(
        self, 
        monthly_bill_ars: Decimal, 
        number_of_panels: int,
        user_email: str = "",
        user_phone: str = ""
    ) -> InvestmentSimulation:
        """
        Simulate investment based on number of panels with tiered pricing:
        - 1-9 panels: $700 USD per panel
        - 10-99 panels: $500 USD per panel  
        - 100+ panels: $400 USD per panel
        
        Applies bill-based restrictions to prevent excessive installations.
        """
        # Apply bill-based restrictions to number of panels
        original_panels = number_of_panels
        number_of_panels = self._apply_bill_restrictions(number_of_panels, monthly_bill_ars)
        
        # Calculate system specifications
        panel_power_kw = self.project.panel_power_wp / 1000
        actual_power_kw = number_of_panels * panel_power_kw
        actual_annual_generation = actual_power_kw * self.annual_generation_factor * self.performance_ratio
        actual_monthly_generation = actual_annual_generation / 12
        
        # Calculate investment using tiered pricing
        total_investment_usd = self._calculate_total_investment_tiered(number_of_panels)
        total_investment_ars = total_investment_usd * self.exchange_rate
        
        # Calculate savings using new formula (based on number of panels)
        monthly_savings_ars = self._calculate_monthly_savings(number_of_panels)
        annual_savings_ars = monthly_savings_ars * 12
        
        # Calculate annual savings in USD using blue exchange rate
        # Formula: (monthly_savings_ars / exchange_rate_blue) * 12
        annual_savings_usd = (monthly_savings_ars / self.exchange_rate) * 12
        
        # Calculate metrics
        payback_period = total_investment_ars / annual_savings_ars if annual_savings_ars > 0 else Decimal('999')
        roi_annual = (annual_savings_ars / total_investment_ars) * 100 if total_investment_ars > 0 else Decimal('0')
        bill_coverage_achieved = (monthly_savings_ars / monthly_bill_ars) * 100
        
        # Create simulation object
        simulation = InvestmentSimulation(
            project=self.project,
            user_email=user_email,
            user_phone=user_phone,
            monthly_bill_ars=monthly_bill_ars,
            tariff_category=self.tariff_category,
            simulation_type='panels',
            number_of_panels=number_of_panels,
            total_investment_usd=total_investment_usd,
            total_investment_ars=total_investment_ars,
            installed_power_kw=actual_power_kw,
            annual_generation_kwh=actual_annual_generation,
            monthly_generation_kwh=actual_monthly_generation,
            monthly_savings_ars=monthly_savings_ars,
            annual_savings_ars=annual_savings_ars,
            payback_period_years=payback_period,
            bill_coverage_achieved=bill_coverage_achieved,
            roi_annual=roi_annual,
            exchange_rate_used=self.exchange_rate
        )
        
        return simulation
    
    def simulate_by_investment(
        self, 
        monthly_bill_ars: Decimal, 
        investment_amount_usd: Decimal,
        user_email: str = "",
        user_phone: str = ""
    ) -> InvestmentSimulation:
        """
        Simulate investment based on investment amount
        Applies bill-based restrictions to prevent excessive investments.
        """
        # Check investment limits based on bill (100% coverage limit)
        limits = self._calculate_bill_based_limits(monthly_bill_ars)
        max_panels_100_coverage = limits['max_panels_for_bill_coverage']
        
        # Calculate maximum investment based on 100% coverage
        max_investment_usd_100_coverage = self._calculate_total_investment_tiered(max_panels_100_coverage)
        
        # Apply investment restriction to 100% coverage limit
        original_investment = investment_amount_usd
        investment_amount_usd = min(investment_amount_usd, max_investment_usd_100_coverage)
        
        # Calculate how many panels can be bought with the investment using tiered pricing
        # We need to reverse-engineer from investment to panels using tiered pricing
        
        # Try different quantities to find how many panels this investment can buy
        max_panels_possible = 1000  # Reasonable upper limit
        best_panels = 0
        
        for test_panels in range(1, max_panels_possible + 1):
            cost_for_panels = self._calculate_total_investment_tiered(test_panels)
            if cost_for_panels <= investment_amount_usd:
                best_panels = test_panels
            else:
                break
        
        # Use the exact number of panels that can be afforded with tiered pricing
        equivalent_panels = Decimal(str(best_panels))
        number_of_panels = best_panels
        
        # Calculate actual power based on the panels we can afford
        panel_power_kw = self.project.panel_power_wp / 1000
        actual_power_kw = equivalent_panels * panel_power_kw
        
        # Keep the user's exact investment amount
        actual_investment_usd = investment_amount_usd
        actual_investment_ars = actual_investment_usd * self.exchange_rate
        
        # Calculate generation based on actual power (not rounded panels)
        actual_annual_generation = actual_power_kw * self.annual_generation_factor * self.performance_ratio
        actual_monthly_generation = actual_annual_generation / 12
        
        # Calculate savings using the same formula as _calculate_monthly_savings
        # But with equivalent fractional panels instead of whole panels
        # Formula: equivalent_panels × 0.66 × precio_energia × 24 × 30 × 0.19
        energy_price_ars = Decimal(str(EnergyPrice.get_current_price()))
        monthly_savings_ars = (
            equivalent_panels * 
            Decimal('0.66') * 
            energy_price_ars * 
            Decimal('24') * 
            Decimal('30') * 
            Decimal('0.19')
        )
        annual_savings_ars = monthly_savings_ars * 12
        
        # Calculate annual savings in USD using blue exchange rate
        # Formula: (monthly_savings_ars / exchange_rate_blue) * 12
        annual_savings_usd = (monthly_savings_ars / self.exchange_rate) * 12
        
        # Calculate metrics
        payback_period = actual_investment_ars / annual_savings_ars if annual_savings_ars > 0 else Decimal('999')
        roi_annual = (annual_savings_ars / actual_investment_ars) * 100 if actual_investment_ars > 0 else Decimal('0')
        bill_coverage_achieved = (monthly_savings_ars / monthly_bill_ars) * 100
        
        # Create simulation object
        simulation = InvestmentSimulation(
            project=self.project,
            user_email=user_email,
            user_phone=user_phone,
            monthly_bill_ars=monthly_bill_ars,
            tariff_category=self.tariff_category,
            simulation_type='investment',
            investment_amount_usd=investment_amount_usd,
            number_of_panels=number_of_panels,
            total_investment_usd=actual_investment_usd,
            total_investment_ars=actual_investment_ars,
            installed_power_kw=actual_power_kw,
            annual_generation_kwh=actual_annual_generation,
            monthly_generation_kwh=actual_monthly_generation,
            monthly_savings_ars=monthly_savings_ars,
            annual_savings_ars=annual_savings_ars,
            payback_period_years=payback_period,
            bill_coverage_achieved=bill_coverage_achieved,
            roi_annual=roi_annual,
            exchange_rate_used=self.exchange_rate
        )
        
        return simulation
    
    def _calculate_tiered_panel_price(self, number_of_panels: int) -> Decimal:
        """
        Calculate panel price based on tiered pricing:
        - 1-9 panels: $700 USD per panel
        - 10-99 panels: $500 USD per panel  
        - 100+ panels: $400 USD per panel
        """
        if number_of_panels <= 9:
            return Decimal('700')
        elif number_of_panels <= 99:
            return Decimal('500')
        else:
            return Decimal('400')
    
    def _calculate_total_investment_tiered(self, number_of_panels: int) -> Decimal:
        """
        Calculate total investment using uniform pricing based on tier:
        - 1-9 panels: $700 USD per panel (ALL panels at $700)
        - 10-99 panels: $500 USD per panel (ALL panels at $500)
        - 100+ panels: $400 USD per panel (ALL panels at $400)
        """
        # Determine the price per panel based on total quantity
        if number_of_panels <= 9:
            price_per_panel = Decimal('700')
        elif number_of_panels <= 99:
            price_per_panel = Decimal('500')
        else:
            price_per_panel = Decimal('400')
        
        total_cost = number_of_panels * price_per_panel
        return total_cost

    def _calculate_monthly_savings(self, number_of_panels: int) -> Decimal:
        """
        Calculate monthly savings based on new formula:
        Ahorro Mensual (ARS) = cant_paneles × 0.66 × precio_energia × 24 × 30 × 0.19
        
        Where:
        - cant_paneles: Number of panels
        - 0.66: Panel efficiency factor
        - precio_energia: Energy price in ARS/kWh (102.25)
        - 24: Hours per day
        - 30: Days per month
        - 0.19: System performance factor
        """
        energy_price_ars = Decimal(str(EnergyPrice.get_current_price()))
        
        monthly_savings_ars = (
            Decimal(str(number_of_panels)) * 
            Decimal('0.66') * 
            energy_price_ars * 
            Decimal('24') * 
            Decimal('30') * 
            Decimal('0.19')
        )
        
        return monthly_savings_ars
    
    def get_project_capacity_check(self, required_power_kw: Decimal) -> Dict[str, Any]:
        """
        Check if the project has enough available capacity
        """
        available_power_kw = self.project.available_power
        
        return {
            'has_capacity': required_power_kw <= available_power_kw,
            'required_power_kw': float(required_power_kw),
            'available_power_kw': float(available_power_kw),
            'utilization_percentage': float((required_power_kw / available_power_kw) * 100) if available_power_kw > 0 else 0
        }
    
    def _calculate_bill_based_limits(self, monthly_bill_ars: Decimal) -> Dict[str, Any]:
        """
        Calculate maximum investment and panels based on monthly bill
        The investment should not exceed what can be recovered through bill savings
        """
        # Calculate maximum reasonable payback period (e.g., 10 years)
        max_payback_years = 10
        max_total_savings = monthly_bill_ars * 12 * max_payback_years  # 10 years of bills
        
        # Convert to USD for investment comparison
        max_investment_ars = max_total_savings
        max_investment_usd = max_investment_ars / self.exchange_rate
        
        # Calculate maximum panels based on what would generate savings equal to the bill
        # For 100% coverage, we need panels that generate monthly_bill_ars in savings
        energy_price_ars = Decimal(str(EnergyPrice.get_current_price()))
        
        # Use the new coverage formula in reverse
        # monthly_bill_ars = number_of_panels * ahorro_por_panel
        # ahorro_por_panel = 0.66 × 101.25 × 24 × 30 × 0.19 = 9,141.66
        ahorro_por_panel = (
            Decimal('0.66') * 
            energy_price_ars * 
            Decimal('24') * 
            Decimal('30') * 
            Decimal('0.19')
        )
        
        max_panels_for_bill = int((monthly_bill_ars / ahorro_por_panel).to_integral_value())
        
        return {
            'max_investment_usd': max_investment_usd,
            'max_investment_ars': max_investment_ars,
            'max_panels_for_bill_coverage': max_panels_for_bill,
            'max_payback_years': max_payback_years,
            'savings_per_panel_ars': ahorro_por_panel
        }
    
    def _apply_bill_restrictions(self, number_of_panels: int, monthly_bill_ars: Decimal) -> int:
        """
        Apply bill-based restrictions to limit number of panels
        Maximum = exactly what's needed for 100% bill coverage (factura total = ahorro mensual)
        """
        limits = self._calculate_bill_based_limits(monthly_bill_ars)
        max_panels = limits['max_panels_for_bill_coverage']
        
        # Limit to exactly 100% coverage: factura_total = ahorro_mensual_ars
        return min(number_of_panels, max_panels)