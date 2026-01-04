"""
MVAI Connexx - Marketing Intelligence & Growth Module
Data-driven marketing strategieën voor revenue growth en customer acquisition
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import database as db
from collections import defaultdict

# ═══════════════════════════════════════════════════════
# MARKETING CHANNELS & CAMPAIGNS
# ═══════════════════════════════════════════════════════

class MarketingChannel(Enum):
    """Marketing acquisition channels"""
    ORGANIC_SEARCH = "organic_search"      # SEO
    PAID_SEARCH = "paid_search"            # Google Ads
    SOCIAL_MEDIA = "social_media"          # LinkedIn, Twitter, Facebook
    CONTENT_MARKETING = "content_marketing"  # Blog, whitepapers
    EMAIL_MARKETING = "email_marketing"    # Email campaigns
    REFERRAL = "referral"                  # Customer referrals
    DIRECT = "direct"                      # Direct traffic
    PARTNER = "partner"                    # Partner channels

class ConversionStage(Enum):
    """Customer journey stages"""
    AWARENESS = "awareness"                # Became aware of product
    INTEREST = "interest"                  # Showed interest
    CONSIDERATION = "consideration"        # Evaluating solution
    TRIAL = "trial"                       # Started trial/demo
    PURCHASE = "purchase"                 # Became paying customer
    RETENTION = "retention"               # Active customer
    ADVOCACY = "advocacy"                 # Referring others

# ═══════════════════════════════════════════════════════
# MARKETING FUNNEL ANALYTICS
# ═══════════════════════════════════════════════════════

class MarketingFunnel:
    """Analyze marketing funnel performance"""

    def __init__(self):
        self.funnel_stages = [
            ConversionStage.AWARENESS,
            ConversionStage.INTEREST,
            ConversionStage.CONSIDERATION,
            ConversionStage.TRIAL,
            ConversionStage.PURCHASE
        ]

    def calculate_funnel_metrics(self, days: int = 30) -> Dict:
        """
        Calculate marketing funnel conversion rates

        Returns metrics for each stage and conversion rates
        """
        with db.get_db() as conn:
            cursor = conn.cursor()

            # Get funnel data from marketing_funnel table
            funnel_data = {}

            for stage in self.funnel_stages:
                cursor.execute('''
                    SELECT COUNT(*) as count
                    FROM marketing_funnel
                    WHERE funnel_stage = ?
                    AND timestamp >= datetime('now', ?)
                ''', (stage.value, f'-{days} days'))

                count = cursor.fetchone()['count']
                funnel_data[stage.value] = count

            # Calculate conversion rates
            conversions = {}
            for i in range(len(self.funnel_stages) - 1):
                current_stage = self.funnel_stages[i]
                next_stage = self.funnel_stages[i + 1]

                current_count = funnel_data[current_stage.value]
                next_count = funnel_data[next_stage.value]

                if current_count > 0:
                    conversion_rate = (next_count / current_count) * 100
                else:
                    conversion_rate = 0

                conversions[f'{current_stage.value}_to_{next_stage.value}'] = round(conversion_rate, 2)

            # Overall funnel conversion (awareness to purchase)
            awareness_count = funnel_data[ConversionStage.AWARENESS.value]
            purchase_count = funnel_data[ConversionStage.PURCHASE.value]
            overall_conversion = (purchase_count / awareness_count * 100) if awareness_count > 0 else 0

            return {
                'period_days': days,
                'funnel_counts': funnel_data,
                'conversion_rates': conversions,
                'overall_conversion_rate': round(overall_conversion, 2),
                'total_awareness': awareness_count,
                'total_purchases': purchase_count,
                'funnel_efficiency': self._calculate_funnel_efficiency(conversions)
            }

    def _calculate_funnel_efficiency(self, conversions: Dict) -> str:
        """Calculate funnel efficiency grade"""
        avg_conversion = sum(conversions.values()) / len(conversions) if conversions else 0

        if avg_conversion >= 50:
            return 'Excellent (A)'
        elif avg_conversion >= 35:
            return 'Good (B)'
        elif avg_conversion >= 20:
            return 'Average (C)'
        elif avg_conversion >= 10:
            return 'Below Average (D)'
        else:
            return 'Poor (F)'

    def identify_funnel_leaks(self, days: int = 30) -> List[Dict]:
        """Identify stages where conversion drops significantly"""
        metrics = self.calculate_funnel_metrics(days)
        conversions = metrics['conversion_rates']

        leaks = []
        for stage_conversion, rate in conversions.items():
            if rate < 25:  # Less than 25% conversion is a leak
                stages = stage_conversion.split('_to_')
                leaks.append({
                    'from_stage': stages[0],
                    'to_stage': stages[2] if len(stages) > 2 else stages[1],
                    'conversion_rate': rate,
                    'severity': 'critical' if rate < 10 else 'high',
                    'recommendation': self._get_leak_recommendation(stages[0])
                })

        return leaks

    def _get_leak_recommendation(self, stage: str) -> str:
        """Get recommendation for fixing funnel leak"""
        recommendations = {
            'awareness': 'Increase SEO efforts, run awareness campaigns, improve brand visibility',
            'interest': 'Improve value proposition, create compelling content, optimize landing pages',
            'consideration': 'Add social proof, case studies, free trial offers',
            'trial': 'Improve onboarding, add product tours, provide better documentation',
            'purchase': 'Simplify checkout, offer discounts, remove friction points'
        }
        return recommendations.get(stage, 'Optimize this stage for better conversion')

# Global funnel instance
marketing_funnel = MarketingFunnel()

# ═══════════════════════════════════════════════════════
# CHANNEL PERFORMANCE ANALYTICS
# ═══════════════════════════════════════════════════════

def get_channel_performance(days: int = 30) -> List[Dict]:
    """Analyze performance of each marketing channel"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                channel,
                COUNT(*) as leads,
                SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) as conversions,
                SUM(cost) as total_cost
            FROM marketing_campaigns
            WHERE created_at >= datetime('now', ?)
            GROUP BY channel
            ORDER BY conversions DESC
        ''', (f'-{days} days',))

        channels = []
        for row in cursor.fetchall():
            leads = row['leads']
            conversions = row['conversions']
            cost = row['total_cost'] or 0

            conversion_rate = (conversions / leads * 100) if leads > 0 else 0
            cost_per_lead = cost / leads if leads > 0 else 0
            cost_per_acquisition = cost / conversions if conversions > 0 else 0

            # ROI calculation (assuming avg customer value of €1000)
            avg_customer_value = 1000  # Placeholder
            roi = ((conversions * avg_customer_value - cost) / cost * 100) if cost > 0 else 0

            channels.append({
                'channel': row['channel'],
                'leads': leads,
                'conversions': conversions,
                'conversion_rate_pct': round(conversion_rate, 2),
                'total_cost': round(cost, 2),
                'cost_per_lead': round(cost_per_lead, 2),
                'cost_per_acquisition': round(cost_per_acquisition, 2),
                'roi_pct': round(roi, 1),
                'grade': _grade_channel_performance(conversion_rate, roi)
            })

        return channels

def _grade_channel_performance(conversion_rate: float, roi: float) -> str:
    """Grade channel performance"""
    score = 0

    # Conversion rate scoring (0-50 points)
    if conversion_rate >= 10:
        score += 50
    elif conversion_rate >= 5:
        score += 35
    elif conversion_rate >= 2:
        score += 20
    else:
        score += 10

    # ROI scoring (0-50 points)
    if roi >= 300:
        score += 50
    elif roi >= 200:
        score += 40
    elif roi >= 100:
        score += 30
    elif roi >= 0:
        score += 20
    else:
        score += 0

    if score >= 90:
        return 'A+'
    elif score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    else:
        return 'D'

# ═══════════════════════════════════════════════════════
# CUSTOMER SEGMENTATION
# ═══════════════════════════════════════════════════════

def get_customer_segments() -> Dict:
    """Segment customers for targeted marketing"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        # Segment by pricing tier (product-based)
        cursor.execute('''
            SELECT
                pricing_tier,
                COUNT(*) as count,
                AVG(CAST((julianday('now') - julianday(created_at)) AS INTEGER)) as avg_age_days
            FROM customers
            WHERE status = 'active'
            GROUP BY pricing_tier
        ''')
        by_tier = [dict(row) for row in cursor.fetchall()]

        # Segment by engagement (behavioral)
        cursor.execute('''
            SELECT
                c.id,
                c.name,
                COUNT(l.id) as log_count,
                MAX(l.timestamp) as last_activity
            FROM customers c
            LEFT JOIN logs l ON c.id = l.customer_id
            WHERE c.status = 'active'
            GROUP BY c.id, c.name
        ''')

        engagement_segments = {
            'champions': [],      # High activity, recent
            'at_risk': [],        # Low activity, not recent
            'new_customers': [],  # < 30 days old
            'loyal': []          # > 180 days, consistent activity
        }

        for row in cursor.fetchall():
            customer_id = row['id']
            log_count = row['log_count']
            last_activity = row['last_activity']

            # Get customer age
            cursor.execute('SELECT created_at FROM customers WHERE id = ?', (customer_id,))
            created_at = datetime.fromisoformat(cursor.fetchone()['created_at'])
            age_days = (datetime.now() - created_at).days

            # Classify
            if age_days < 30:
                engagement_segments['new_customers'].append(row['name'])
            elif age_days > 180 and log_count > 100:
                engagement_segments['loyal'].append(row['name'])
            elif log_count > 50:
                engagement_segments['champions'].append(row['name'])
            elif log_count < 10 or (last_activity and (datetime.now() - datetime.fromisoformat(last_activity)).days > 30):
                engagement_segments['at_risk'].append(row['name'])

        return {
            'by_tier': by_tier,
            'by_engagement': {
                k: {'count': len(v), 'customers': v[:10]}  # Top 10 for display
                for k, v in engagement_segments.items()
            },
            'total_segments': len(engagement_segments)
        }

# ═══════════════════════════════════════════════════════
# GROWTH STRATEGIES
# ═══════════════════════════════════════════════════════

def get_growth_strategies() -> List[Dict]:
    """Generate data-driven growth strategies"""
    strategies = []

    # Strategy 1: Optimize best-performing channel
    channels = get_channel_performance(30)
    if channels:
        best_channel = max(channels, key=lambda x: x['roi_pct'])
        strategies.append({
            'priority': 'high',
            'strategy': 'Double Down on Best Channel',
            'channel': best_channel['channel'],
            'current_roi': f"{best_channel['roi_pct']}%",
            'action': f"Increase budget for {best_channel['channel']} by 50%",
            'expected_impact': f"Additional {best_channel['conversions'] * 0.5:.0f} customers/month",
            'investment_needed': f"€{best_channel['total_cost'] * 0.5:.2f}/month"
        })

    # Strategy 2: Fix funnel leaks
    leaks = marketing_funnel.identify_funnel_leaks(30)
    if leaks:
        worst_leak = min(leaks, key=lambda x: x['conversion_rate'])
        strategies.append({
            'priority': 'high',
            'strategy': 'Fix Critical Funnel Leak',
            'stage': f"{worst_leak['from_stage']} → {worst_leak['to_stage']}",
            'current_conversion': f"{worst_leak['conversion_rate']}%",
            'action': worst_leak['recommendation'],
            'expected_impact': 'Increase overall conversion by 20-30%',
            'investment_needed': '€500-1000 for optimization'
        })

    # Strategy 3: Reactivate at-risk customers
    segments = get_customer_segments()
    at_risk_count = segments['by_engagement']['at_risk']['count']
    if at_risk_count > 0:
        strategies.append({
            'priority': 'medium',
            'strategy': 'Win-Back Campaign for At-Risk Customers',
            'target_segment': 'at_risk',
            'customer_count': at_risk_count,
            'action': 'Email campaign with special offer (20% discount for 3 months)',
            'expected_impact': f'Reactivate {at_risk_count * 0.3:.0f} customers (30% success rate)',
            'investment_needed': f'€{at_risk_count * 2:.2f} (email costs + discount)'
        })

    # Strategy 4: Upsell loyal customers
    loyal_count = segments['by_engagement']['loyal']['count']
    if loyal_count > 0:
        strategies.append({
            'priority': 'high',
            'strategy': 'Upsell Loyal Customers to Higher Tier',
            'target_segment': 'loyal',
            'customer_count': loyal_count,
            'action': 'Personalized outreach with feature upgrade benefits',
            'expected_impact': f'{loyal_count * 0.2:.0f} upgrades (20% conversion)',
            'revenue_increase': f'€{loyal_count * 0.2 * 70:.2f}/month (avg €70 MRR increase)'
        })

    # Strategy 5: Referral program
    strategies.append({
        'priority': 'medium',
        'strategy': 'Launch Referral Program',
        'action': 'Offer 1 month free for each successful referral',
        'expected_impact': '15-25% of customers will refer (avg 1.2 referrals each)',
        'investment_needed': 'Low (automated system + reward costs)',
        'payback_period': '2-3 months'
    })

    return strategies

# ═══════════════════════════════════════════════════════
# CAMPAIGN ROI TRACKER
# ═══════════════════════════════════════════════════════

def track_campaign_roi(campaign_id: Optional[int] = None, days: int = 30) -> Dict:
    """Track ROI for marketing campaigns"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        if campaign_id:
            # Specific campaign
            cursor.execute('''
                SELECT * FROM marketing_campaigns
                WHERE id = ?
            ''', (campaign_id,))
            campaigns = [dict(cursor.fetchone())]
        else:
            # All recent campaigns
            cursor.execute('''
                SELECT * FROM marketing_campaigns
                WHERE created_at >= datetime('now', ?)
                ORDER BY created_at DESC
            ''', (f'-{days} days',))
            campaigns = [dict(row) for row in cursor.fetchall()]

    results = []
    for campaign in campaigns:
        if not campaign:
            continue

        cost = campaign.get('cost', 0) or 0
        conversions = campaign.get('conversions', 0) or 0

        # Calculate ROI (using €1000 avg customer value)
        avg_customer_value = 1000
        revenue = conversions * avg_customer_value
        roi = ((revenue - cost) / cost * 100) if cost > 0 else 0

        results.append({
            'campaign_id': campaign['id'],
            'campaign_name': campaign.get('name', 'Unnamed'),
            'channel': campaign.get('channel', 'unknown'),
            'cost': cost,
            'conversions': conversions,
            'revenue': revenue,
            'roi_pct': round(roi, 1),
            'roi_grade': 'Excellent' if roi > 300 else 'Good' if roi > 100 else 'Poor'
        })

    return {
        'campaigns': results,
        'total_cost': sum(c['cost'] for c in results),
        'total_revenue': sum(c['revenue'] for c in results),
        'avg_roi': round(sum(c['roi_pct'] for c in results) / len(results), 1) if results else 0
    }

# ═══════════════════════════════════════════════════════
# LEAD SCORING
# ═══════════════════════════════════════════════════════

def calculate_lead_score(lead_data: Dict) -> int:
    """
    Calculate lead score (0-100) based on attributes

    Higher score = higher probability to convert
    """
    score = 0

    # Company size (employees)
    company_size = lead_data.get('company_size', 0)
    if company_size > 500:
        score += 30
    elif company_size > 100:
        score += 20
    elif company_size > 20:
        score += 10

    # Industry fit
    target_industries = ['logistics', 'transport', 'supply_chain', 'warehousing']
    if lead_data.get('industry', '').lower() in target_industries:
        score += 25

    # Engagement level
    page_views = lead_data.get('page_views', 0)
    if page_views > 10:
        score += 15
    elif page_views > 5:
        score += 10
    elif page_views > 2:
        score += 5

    # Content downloads
    if lead_data.get('downloaded_whitepaper'):
        score += 10

    # Demo request
    if lead_data.get('requested_demo'):
        score += 20

    return min(100, score)

def get_lead_recommendations(lead_score: int) -> str:
    """Get sales action recommendation based on lead score"""
    if lead_score >= 70:
        return 'HOT - Contact immediately for demo'
    elif lead_score >= 50:
        return 'WARM - Nurture with targeted content, schedule call'
    elif lead_score >= 30:
        return 'COLD - Add to email drip campaign'
    else:
        return 'NOT QUALIFIED - Revisit in 3 months'

# ═══════════════════════════════════════════════════════
# MARKETING DASHBOARD
# ═══════════════════════════════════════════════════════

def get_marketing_dashboard() -> Dict:
    """Complete marketing intelligence dashboard"""
    funnel_metrics = marketing_funnel.calculate_funnel_metrics(30)
    channel_performance = get_channel_performance(30)
    segments = get_customer_segments()
    growth_strategies = get_growth_strategies()
    campaign_roi = track_campaign_roi(days=30)

    return {
        'funnel': funnel_metrics,
        'channels': channel_performance,
        'segments': segments,
        'growth_strategies': growth_strategies,
        'campaign_performance': campaign_roi,
        'top_channel': max(channel_performance, key=lambda x: x['roi_pct']) if channel_performance else None,
        'summary': {
            'total_leads_30d': funnel_metrics['total_awareness'],
            'total_conversions_30d': funnel_metrics['total_purchases'],
            'overall_conversion_rate': funnel_metrics['overall_conversion_rate'],
            'avg_campaign_roi': campaign_roi['avg_roi'],
            'at_risk_customers': segments['by_engagement']['at_risk']['count']
        }
    }

if __name__ == '__main__':
    print("✓ Marketing Intelligence Module loaded")
    dashboard = get_marketing_dashboard()
    print(f"✓ Conversion Rate: {dashboard['summary']['overall_conversion_rate']}%")
    print(f"✓ Avg Campaign ROI: {dashboard['summary']['avg_campaign_roi']}%")
