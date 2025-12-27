"""
MVAI Connexx - Advanced Analytics Module
Real-time metrics, trends en advanced reporting
"""
from datetime import datetime, timedelta
import database as db
from collections import defaultdict

def get_customer_analytics(customer_id, days=30):
    """Uitgebreide analytics voor specifieke klant"""

    # Basis stats
    stats = db.get_customer_stats(customer_id)

    # Haal alle logs van afgelopen X dagen
    with db.get_db() as conn:
        cursor = conn.cursor()

        # Daily activity (laatste 30 dagen)
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM logs
            WHERE customer_id = ?
            AND timestamp >= DATE('now', ?)
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''', (customer_id, f'-{days} days'))

        daily_activity = [
            {'date': row['date'], 'count': row['count']}
            for row in cursor.fetchall()
        ]

        # Hourly distribution (alle tijd)
        cursor.execute('''
            SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
            FROM logs
            WHERE customer_id = ?
            GROUP BY hour
            ORDER BY hour
        ''', (customer_id,))

        hourly_distribution = [
            {'hour': int(row['hour']), 'count': row['count']}
            for row in cursor.fetchall()
        ]

        # IP diversity
        cursor.execute('''
            SELECT ip_address, COUNT(*) as count
            FROM logs
            WHERE customer_id = ?
            GROUP BY ip_address
            ORDER BY count DESC
            LIMIT 10
        ''', (customer_id,))

        top_ips = [
            {'ip': row['ip_address'], 'count': row['count']}
            for row in cursor.fetchall()
        ]

        # Weekly trend
        cursor.execute('''
            SELECT strftime('%Y-%W', timestamp) as week, COUNT(*) as count
            FROM logs
            WHERE customer_id = ?
            AND timestamp >= DATE('now', '-12 weeks')
            GROUP BY week
            ORDER BY week
        ''', (customer_id,))

        weekly_trend = [
            {'week': row['week'], 'count': row['count']}
            for row in cursor.fetchall()
        ]

        # Growth rate (comparison met vorige periode)
        cursor.execute('''
            SELECT COUNT(*) as current_period
            FROM logs
            WHERE customer_id = ?
            AND timestamp >= DATE('now', '-7 days')
        ''', (customer_id,))
        current_period = cursor.fetchone()['current_period']

        cursor.execute('''
            SELECT COUNT(*) as previous_period
            FROM logs
            WHERE customer_id = ?
            AND timestamp >= DATE('now', '-14 days')
            AND timestamp < DATE('now', '-7 days')
        ''', (customer_id,))
        previous_period = cursor.fetchone()['previous_period']

        if previous_period > 0:
            growth_rate = ((current_period - previous_period) / previous_period) * 100
        else:
            growth_rate = 100 if current_period > 0 else 0

    return {
        **stats,
        'daily_activity': daily_activity,
        'hourly_distribution': hourly_distribution,
        'top_ips': top_ips,
        'weekly_trend': weekly_trend,
        'growth_rate': round(growth_rate, 2),
        'current_week_logs': current_period,
        'previous_week_logs': previous_period
    }

def get_global_analytics():
    """Globale analytics voor admin dashboard"""

    with db.get_db() as conn:
        cursor = conn.cursor()

        # Customer growth over time
        cursor.execute('''
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM customers
            GROUP BY DATE(created_at)
            ORDER BY date
        ''')

        customer_growth = [
            {'date': row['date'], 'count': row['count']}
            for row in cursor.fetchall()
        ]

        # Total logs per day (laatste 30 dagen)
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM logs
            WHERE timestamp >= DATE('now', '-30 days')
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''')

        daily_logs = [
            {'date': row['date'], 'count': row['count']}
            for row in cursor.fetchall()
        ]

        # Customer status breakdown
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM customers
            GROUP BY status
        ''')

        status_breakdown = {
            row['status']: row['count']
            for row in cursor.fetchall()
        }

        # Most active customers (laatste 7 dagen)
        cursor.execute('''
            SELECT c.name, COUNT(l.id) as log_count
            FROM customers c
            LEFT JOIN logs l ON c.id = l.customer_id
            WHERE l.timestamp >= DATE('now', '-7 days')
            GROUP BY c.id
            ORDER BY log_count DESC
            LIMIT 10
        ''')

        active_customers = [
            {'name': row['name'], 'log_count': row['log_count']}
            for row in cursor.fetchall()
        ]

        # Average logs per customer
        cursor.execute('''
            SELECT AVG(log_count) as avg_logs
            FROM (
                SELECT COUNT(*) as log_count
                FROM logs
                GROUP BY customer_id
            )
        ''')

        avg_logs = cursor.fetchone()['avg_logs'] or 0

        # System health metrics
        cursor.execute('SELECT COUNT(*) FROM customers WHERE status = "active"')
        active_customers_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM logs')
        total_logs = cursor.fetchone()[0]

        cursor.execute('''
            SELECT COUNT(*) FROM logs
            WHERE timestamp >= DATE('now', '-1 day')
        ''')
        logs_last_24h = cursor.fetchone()[0]

    return {
        'customer_growth': customer_growth,
        'daily_logs': daily_logs,
        'status_breakdown': status_breakdown,
        'active_customers': active_customers,
        'avg_logs_per_customer': round(avg_logs, 2),
        'total_active_customers': active_customers_count,
        'total_logs': total_logs,
        'logs_last_24h': logs_last_24h,
        'system_health': 'healthy' if logs_last_24h > 0 else 'idle'
    }

def get_customer_predictions(customer_id):
    """Voorspel toekomstige activity patterns"""

    with db.get_db() as conn:
        cursor = conn.cursor()

        # Haal laatste 4 weken op voor trend analysis
        cursor.execute('''
            SELECT
                strftime('%Y-%W', timestamp) as week,
                COUNT(*) as count
            FROM logs
            WHERE customer_id = ?
            AND timestamp >= DATE('now', '-4 weeks')
            GROUP BY week
            ORDER BY week
        ''', (customer_id,))

        weeks = [row['count'] for row in cursor.fetchall()]

        if len(weeks) >= 2:
            # Simpele lineaire trend
            avg_growth = sum(weeks[i] - weeks[i-1] for i in range(1, len(weeks))) / (len(weeks) - 1)
            predicted_next_week = max(0, int(weeks[-1] + avg_growth))
        else:
            predicted_next_week = weeks[0] if weeks else 0
            avg_growth = 0

    return {
        'predicted_next_week': predicted_next_week,
        'trend': 'growing' if avg_growth > 0 else 'declining' if avg_growth < 0 else 'stable',
        'weekly_data': weeks
    }

def get_audit_logs(limit=50, customer_id=None, action_type=None):
    """Haal audit logs op met filters"""

    with db.get_db() as conn:
        cursor = conn.cursor()

        query = 'SELECT * FROM audit_logs WHERE 1=1'
        params = []

        if customer_id:
            query += ' AND customer_id = ?'
            params.append(customer_id)

        if action_type:
            query += ' AND action = ?'
            params.append(action_type)

        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

if __name__ == '__main__':
    # Test analytics
    db.init_db()
    print("Analytics module loaded successfully")
