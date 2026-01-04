"""
MVAI Connexx - Unit Economics & Business Metrics Module
Enterprise-grade business intelligence voor profitability en growth tracking
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from decimal import Decimal
import database as db
from collections import defaultdict

# ═══════════════════════════════════════════════════════
# PRICING & COST CONFIGURATION
# ═══════════════════════════════════════════════════════

class PricingConfig:
    """Configuratie voor pricing en costs"""

    # PRICING TIERS (maandelijks in EUR)
    PRICING_TIERS = {
        'demo': {
            'price_per_month': 0.00,
            'included_logs': 100,
            'overage_per_1k_logs': 0.00,
            'max_api_calls': 1000,
            'features': ['basic_analytics', 'csv_export'],
            'description': 'Free demo account - 14 dagen trial'
        },
        'particulier': {
            'price_per_month': 19.00,
            'included_logs': 500,
            'overage_per_1k_logs': 3.00,
            'max_api_calls': 5000,
            'features': ['basic_analytics', 'csv_export', 'mobile_app'],
            'description': 'Perfect voor particulieren en zelfstandigen'
        },
        'mkb': {
            'price_per_month': 49.00,
            'included_logs': 5000,
            'overage_per_1k_logs': 2.50,
            'max_api_calls': 50000,
            'features': ['advanced_analytics', 'api_access', 'priority_support'],
            'description': 'Ideaal voor MKB bedrijven (1-50 medewerkers)'
        },
        'starter': {
            'price_per_month': 29.00,
            'included_logs': 1000,
            'overage_per_1k_logs': 5.00,
            'max_api_calls': 10000,
            'features': ['basic_analytics', 'csv_export'],
            'description': 'Starter pakket voor kleine bedrijven'
        },
        'professional': {
            'price_per_month': 99.00,
            'included_logs': 10000,
            'overage_per_1k_logs': 3.00,
            'max_api_calls': 100000,
            'features': ['advanced_analytics', 'api_access', 'ai_assistant'],
            'description': 'Professional pakket voor groeiende bedrijven'
        },
        'enterprise': {
            'price_per_month': 299.00,
            'included_logs': 100000,
            'overage_per_1k_logs': 1.50,
            'max_api_calls': 1000000,
            'features': ['all_features', 'dedicated_support', 'custom_integration', 'sla_guarantee'],
            'description': 'Enterprise pakket met 99.9% SLA garantie'
        }
    }

    # OPERATIONAL COSTS (per maand)
    COSTS = {
        'hosting_per_customer': 5.00,        # Fly.io hosting cost per customer
        'database_storage_gb': 0.10,         # Storage cost per GB
        'api_call_per_1k': 0.05,             # API infrastructure cost
        'support_per_customer': 10.00,       # Support overhead per customer
        'development_monthly': 2000.00,      # Fixed development cost
        'infrastructure_fixed': 100.00,      # Fixed infrastructure costs
        'marketing_cac_target': 50.00        # Target Customer Acquisition Cost
    }

# ═══════════════════════════════════════════════════════
# UNIT ECONOMICS CALCULATOR
# ═══════════════════════════════════════════════════════

class UnitEconomicsCalculator:
    """Calculate unit economics metrics"""

    def __init__(self):
        self.pricing = PricingConfig.PRICING_TIERS
        self.costs = PricingConfig.COSTS

    def calculate_customer_ltv(self, customer_id: int) -> Dict:
        """
        Calculate Customer Lifetime Value (LTV)

        LTV = (Average Monthly Revenue) × (Customer Lifetime in Months)
        """
        with db.get_db() as conn:
            cursor = conn.cursor()

            # Get customer data
            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Customer with id {customer_id} not found")
            customer = dict(row)

            # Get pricing tier
            tier = customer.get('pricing_tier', 'starter')
            monthly_price = self.pricing[tier]['price_per_month']

            # Calculate months active
            created_at = datetime.fromisoformat(customer['created_at'])
            months_active = max(1, (datetime.now() - created_at).days / 30)

            # Get usage data for overage calculation
            cursor.execute('''
                SELECT COUNT(*) as total_logs
                FROM logs
                WHERE customer_id = ?
            ''', (customer_id,))
            total_logs = cursor.fetchone()['total_logs']

            # Calculate overage charges
            included_logs = self.pricing[tier]['included_logs']
            overage_logs = max(0, total_logs - (included_logs * months_active))
            overage_charge = (overage_logs / 1000) * self.pricing[tier]['overage_per_1k_logs']

            # Total revenue from this customer
            total_revenue = (monthly_price * months_active) + overage_charge

            # Average monthly revenue
            avg_monthly_revenue = total_revenue / months_active if months_active > 0 else monthly_price

            # Estimated customer lifetime (months) - based on churn rate
            estimated_lifetime_months = 24  # Assumption: 24 month avg lifetime

            # Calculate LTV
            ltv = avg_monthly_revenue * estimated_lifetime_months

            return {
                'customer_id': customer_id,
                'pricing_tier': tier,
                'months_active': round(months_active, 1),
                'monthly_recurring_revenue': monthly_price,
                'overage_revenue': round(overage_charge, 2),
                'total_revenue_to_date': round(total_revenue, 2),
                'avg_monthly_revenue': round(avg_monthly_revenue, 2),
                'estimated_lifetime_months': estimated_lifetime_months,
                'lifetime_value': round(ltv, 2)
            }

    def calculate_customer_cac(self, customer_id: int) -> Dict:
        """
        Calculate Customer Acquisition Cost (CAC)

        CAC = Total Marketing & Sales Costs / Number of Customers Acquired
        """
        # For now, use target CAC from config
        # In production, track actual marketing spend per customer
        cac = self.costs['marketing_cac_target']

        ltv_data = self.calculate_customer_ltv(customer_id)
        ltv = ltv_data['lifetime_value']

        # Calculate LTV:CAC ratio
        ltv_cac_ratio = ltv / cac if cac > 0 else 0

        return {
            'customer_id': customer_id,
            'customer_acquisition_cost': cac,
            'lifetime_value': ltv,
            'ltv_cac_ratio': round(ltv_cac_ratio, 2),
            'is_profitable': ltv_cac_ratio > 3.0,  # Industry standard: LTV:CAC should be >3:1
            'payback_period_months': round(cac / ltv_data['avg_monthly_revenue'], 1) if ltv_data['avg_monthly_revenue'] > 0 else 0
        }

    def calculate_monthly_costs_per_customer(self, customer_id: int) -> Dict:
        """Calculate monthly operational costs per customer"""
        with db.get_db() as conn:
            cursor = conn.cursor()

            # Get usage stats for last 30 days
            cursor.execute('''
                SELECT COUNT(*) as logs_30d
                FROM logs
                WHERE customer_id = ?
                AND timestamp >= datetime('now', '-30 days')
            ''', (customer_id,))
            logs_30d = cursor.fetchone()['logs_30d']

            # Get API usage (from api_keys table)
            cursor.execute('''
                SELECT SUM(usage_count) as api_calls
                FROM api_keys
                WHERE customer_id = ?
            ''', (customer_id,))
            api_calls = cursor.fetchone()['api_calls'] or 0

        # Calculate costs
        hosting_cost = self.costs['hosting_per_customer']
        support_cost = self.costs['support_per_customer']

        # Storage cost (estimate: 1KB per log average)
        storage_gb = (logs_30d * 1024) / (1024**3)
        storage_cost = storage_gb * self.costs['database_storage_gb']

        # API cost
        api_cost = (api_calls / 1000) * self.costs['api_call_per_1k']

        total_cost = hosting_cost + support_cost + storage_cost + api_cost

        return {
            'customer_id': customer_id,
            'hosting_cost': round(hosting_cost, 2),
            'support_cost': round(support_cost, 2),
            'storage_cost': round(storage_cost, 2),
            'api_cost': round(api_cost, 2),
            'total_monthly_cost': round(total_cost, 2),
            'logs_30d': logs_30d,
            'api_calls_30d': api_calls
        }

    def calculate_customer_profitability(self, customer_id: int) -> Dict:
        """Calculate overall customer profitability"""
        ltv_data = self.calculate_customer_ltv(customer_id)
        costs_data = self.calculate_monthly_costs_per_customer(customer_id)
        cac_data = self.calculate_customer_cac(customer_id)

        # Monthly profit
        monthly_revenue = ltv_data['avg_monthly_revenue']
        monthly_cost = costs_data['total_monthly_cost']
        monthly_profit = monthly_revenue - monthly_cost

        # Profit margin
        profit_margin = (monthly_profit / monthly_revenue * 100) if monthly_revenue > 0 else 0

        # Total profit to date (revenue - costs - CAC)
        total_revenue = ltv_data['total_revenue_to_date']
        total_costs = monthly_cost * ltv_data['months_active']
        total_profit = total_revenue - total_costs - cac_data['customer_acquisition_cost']

        return {
            'customer_id': customer_id,
            'monthly_revenue': round(monthly_revenue, 2),
            'monthly_cost': round(monthly_cost, 2),
            'monthly_profit': round(monthly_profit, 2),
            'profit_margin_pct': round(profit_margin, 1),
            'total_profit_to_date': round(total_profit, 2),
            'is_profitable': monthly_profit > 0,
            'payback_achieved': total_profit > 0,
            'grade': self._calculate_profitability_grade(profit_margin, cac_data['ltv_cac_ratio'])
        }

    def _calculate_profitability_grade(self, profit_margin: float, ltv_cac_ratio: float) -> str:
        """
        Calculate profitability grade (A+ to F)

        Grading criteria:
        - Profit margin
        - LTV:CAC ratio
        """
        score = 0

        # Profit margin scoring (0-50 points)
        if profit_margin >= 60:
            score += 50
        elif profit_margin >= 40:
            score += 40
        elif profit_margin >= 20:
            score += 30
        elif profit_margin >= 0:
            score += 20
        else:
            score += 0

        # LTV:CAC ratio scoring (0-50 points)
        if ltv_cac_ratio >= 5.0:
            score += 50
        elif ltv_cac_ratio >= 4.0:
            score += 40
        elif ltv_cac_ratio >= 3.0:
            score += 30
        elif ltv_cac_ratio >= 2.0:
            score += 20
        else:
            score += 10

        # Convert to grade
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        elif score >= 45:
            return 'D'
        else:
            return 'F'

# Global calculator instance
unit_economics = UnitEconomicsCalculator()

# ═══════════════════════════════════════════════════════
# BUSINESS METRICS DASHBOARD
# ═══════════════════════════════════════════════════════

def get_business_metrics() -> Dict:
    """Get overall business metrics"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        # Total customers
        cursor.execute('SELECT COUNT(*) as total FROM customers WHERE status = "active"')
        total_customers = cursor.fetchone()['total']

        # Monthly Recurring Revenue (MRR)
        cursor.execute('''
            SELECT pricing_tier, COUNT(*) as count
            FROM customers
            WHERE status = 'active'
            GROUP BY pricing_tier
        ''')
        tier_counts = {row['pricing_tier']: row['count'] for row in cursor.fetchall()}

        mrr = sum(
            tier_counts.get(tier, 0) * PricingConfig.PRICING_TIERS[tier]['price_per_month']
            for tier in PricingConfig.PRICING_TIERS.keys()
        )

        # Annual Recurring Revenue (ARR)
        arr = mrr * 12

        # Total costs
        variable_costs = total_customers * (
            PricingConfig.COSTS['hosting_per_customer'] +
            PricingConfig.COSTS['support_per_customer']
        )
        fixed_costs = (
            PricingConfig.COSTS['development_monthly'] +
            PricingConfig.COSTS['infrastructure_fixed']
        )
        total_monthly_costs = variable_costs + fixed_costs

        # Gross profit
        gross_profit = mrr - total_monthly_costs
        gross_margin = (gross_profit / mrr * 100) if mrr > 0 else 0

        # Customer metrics
        cursor.execute('''
            SELECT AVG(
                CAST((julianday('now') - julianday(created_at)) AS INTEGER)
            ) as avg_age_days
            FROM customers
            WHERE status = 'active'
        ''')
        avg_customer_age_days = cursor.fetchone()['avg_age_days'] or 0

        # Churn rate (simplified - customers deactivated in last 30 days)
        cursor.execute('''
            SELECT COUNT(*) as churned
            FROM customers
            WHERE status = 'inactive'
            AND updated_at >= datetime('now', '-30 days')
        ''')
        churned_30d = cursor.fetchone()['churned']
        churn_rate = (churned_30d / total_customers * 100) if total_customers > 0 else 0

        # Customer distribution by tier
        customer_distribution = {
            tier: tier_counts.get(tier, 0)
            for tier in PricingConfig.PRICING_TIERS.keys()
        }

        return {
            'total_active_customers': total_customers,
            'mrr': round(mrr, 2),
            'arr': round(arr, 2),
            'total_monthly_costs': round(total_monthly_costs, 2),
            'gross_profit': round(gross_profit, 2),
            'gross_margin_pct': round(gross_margin, 1),
            'avg_customer_age_days': round(avg_customer_age_days, 1),
            'churn_rate_pct': round(churn_rate, 2),
            'customer_distribution': customer_distribution,
            'break_even_customers': round(fixed_costs / (
                PricingConfig.PRICING_TIERS['starter']['price_per_month'] -
                PricingConfig.COSTS['hosting_per_customer'] -
                PricingConfig.COSTS['support_per_customer']
            )),
            'runway_months': round(gross_profit / fixed_costs, 1) if gross_profit > 0 else 0
        }

def get_customer_grades() -> List[Dict]:
    """Get profitability grades for all customers"""
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM customers WHERE status = "active"')
        customers = [dict(row) for row in cursor.fetchall()]

    results = []
    for customer in customers:
        profitability = unit_economics.calculate_customer_profitability(customer['id'])
        results.append({
            'customer_id': customer['id'],
            'customer_name': customer['name'],
            'grade': profitability['grade'],
            'monthly_profit': profitability['monthly_profit'],
            'profit_margin_pct': profitability['profit_margin_pct']
        })

    # Sort by grade
    grade_order = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
    results.sort(key=lambda x: grade_order.index(x['grade']))

    return results

def get_pricing_recommendations(customer_id: int) -> Dict:
    """Get pricing tier recommendations voor customer"""
    profitability = unit_economics.calculate_customer_profitability(customer_id)
    ltv_data = unit_economics.calculate_customer_ltv(customer_id)

    current_tier = ltv_data['pricing_tier']
    current_mrr = ltv_data['monthly_recurring_revenue']

    recommendations = []

    # If profit margin < 30%, suggest upgrade
    if profitability['profit_margin_pct'] < 30:
        tier_upgrades = {
            'starter': 'professional',
            'professional': 'enterprise',
            'enterprise': None
        }
        next_tier = tier_upgrades.get(current_tier)

        if next_tier:
            new_mrr = PricingConfig.PRICING_TIERS[next_tier]['price_per_month']
            recommendations.append({
                'action': 'upgrade',
                'from_tier': current_tier,
                'to_tier': next_tier,
                'current_mrr': current_mrr,
                'new_mrr': new_mrr,
                'additional_revenue': new_mrr - current_mrr,
                'reason': f'Current profit margin ({profitability["profit_margin_pct"]:.1f}%) is below target (30%)'
            })

    # If profit margin > 60%, could offer discount or add features
    if profitability['profit_margin_pct'] > 60:
        recommendations.append({
            'action': 'retain',
            'reason': f'Excellent profit margin ({profitability["profit_margin_pct"]:.1f}%). Consider loyalty rewards or feature upgrades.',
            'suggestion': 'Offer annual discount (10%) to lock in long-term commitment'
        })

    return {
        'customer_id': customer_id,
        'current_tier': current_tier,
        'profitability_grade': profitability['grade'],
        'recommendations': recommendations
    }

# ═══════════════════════════════════════════════════════
# COHORT ANALYSIS
# ═══════════════════════════════════════════════════════

def get_cohort_analysis(months_back: int = 6) -> Dict:
    """Analyze customer cohorts by signup month"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                strftime('%Y-%m', created_at) as cohort_month,
                COUNT(*) as customers,
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active,
                pricing_tier
            FROM customers
            WHERE created_at >= datetime('now', ?)
            GROUP BY cohort_month, pricing_tier
            ORDER BY cohort_month DESC
        ''', (f'-{months_back} months',))

        cohorts = defaultdict(lambda: {'total': 0, 'active': 0, 'by_tier': {}})

        for row in cursor.fetchall():
            month = row['cohort_month']
            cohorts[month]['total'] += row['customers']
            cohorts[month]['active'] += row['active']
            cohorts[month]['by_tier'][row['pricing_tier']] = row['customers']

        # Calculate retention rates
        for month, data in cohorts.items():
            data['retention_rate'] = round(
                (data['active'] / data['total'] * 100) if data['total'] > 0 else 0,
                1
            )

        return dict(cohorts)

if __name__ == '__main__':
    print("✓ Unit Economics Module loaded")
    metrics = get_business_metrics()
    print(f"✓ MRR: €{metrics['mrr']}")
    print(f"✓ ARR: €{metrics['arr']}")
    print(f"✓ Gross Margin: {metrics['gross_margin_pct']}%")
