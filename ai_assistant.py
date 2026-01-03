"""
MVAI Connexx - AI Assistant Module
Geïsoleerde AI Secretaresse per klant met opt-in systeem
"""
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict
import database as db

# ═══════════════════════════════════════════════════════
# AI ASSISTANT PER KLANT (GEÏSOLEERD)
# ═══════════════════════════════════════════════════════

class AIAssistant:
    """
    Persoonlijke AI Secretaresse voor elke klant
    - Volledig geïsoleerd (klant data blijft privé)
    - Alleen actief met klant toestemming
    - Leert van klant gedrag
    - Proactieve suggesties
    """

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.enabled = self.check_if_enabled()
        self.preferences = self.load_preferences()
        self.conversation_history = []
        self.learned_patterns = {}

    def check_if_enabled(self):
        """Check of klant AI Assistant heeft geactiveerd"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ai_assistant_enabled FROM customers WHERE id = ?
            ''', (self.customer_id,))
            row = cursor.fetchone()
            return row['ai_assistant_enabled'] if row else False

    def load_preferences(self):
        """Laad AI voorkeuren van klant"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM ai_assistant_preferences WHERE customer_id = ?
            ''', (self.customer_id,))
            row = cursor.fetchone()

            if row:
                return {
                    'language': row['language'] or 'nl',
                    'tone': row['tone'] or 'professional',
                    'proactive': row['proactive_suggestions'],
                    'auto_report': row['auto_reports'],
                    'notifications': row['notifications_enabled']
                }

        # Default settings
        return {
            'language': 'nl',
            'tone': 'professional',
            'proactive': True,
            'auto_report': False,
            'notifications': True
        }

    # ══════════════════════════════════════════════════
    # NATURAL LANGUAGE PROCESSING
    # ══════════════════════════════════════════════════

    def process_command(self, user_input):
        """
        Verwerk natuurlijke taal commando's

        Voorbeelden:
        - "Maak een rapport van afgelopen week"
        - "Hoeveel logs waren er vandaag?"
        - "Laat trend zien van deze maand"
        - "Stuur me een samenvatting"
        """
        if not self.enabled:
            return {
                'success': False,
                'message': 'AI Assistant is niet geactiveerd. Ga naar instellingen om te activeren.'
            }

        user_input = user_input.lower().strip()

        # Detecteer intent
        intent = self._detect_intent(user_input)

        # Verwerk gebaseerd op intent
        if intent == 'create_report':
            return self._create_report(user_input)

        elif intent == 'get_stats':
            return self._get_statistics(user_input)

        elif intent == 'show_trend':
            return self._show_trend(user_input)

        elif intent == 'summarize':
            return self._create_summary(user_input)

        elif intent == 'search':
            return self._search_data(user_input)

        elif intent == 'reminder':
            return self._set_reminder(user_input)

        elif intent == 'help':
            return self._get_help()

        else:
            return {
                'success': False,
                'message': 'Ik begrijp het commando niet. Typ "help" voor voorbeelden.',
                'suggestions': self._get_suggestions()
            }

    def _detect_intent(self, text):
        """Detecteer wat gebruiker wil"""
        patterns = {
            'create_report': r'(maak|genereer|creëer).*(rapport|report)',
            'get_stats': r'(hoeveel|aantal|stats|statistiek)',
            'show_trend': r'(laat|toon|zie).*(trend|patroon|grafiek)',
            'summarize': r'(samenvatting|overzicht|recap)',
            'search': r'(zoek|vind|search)',
            'reminder': r'(herinner|reminder|notificatie)',
            'help': r'(help|hulp|wat kan)'
        }

        for intent, pattern in patterns.items():
            if re.search(pattern, text):
                return intent

        return 'unknown'

    # ══════════════════════════════════════════════════
    # AI FUNCTIONS
    # ══════════════════════════════════════════════════

    def _create_report(self, text):
        """Genereer rapport op basis van request"""
        # Detecteer tijdsperiode
        period = self._extract_time_period(text)

        # Haal data op
        logs = db.get_customer_logs(self.customer_id, limit=1000)

        # Filter op periode
        if period:
            logs = [
                log for log in logs
                if self._is_in_period(log['timestamp'], period)
            ]

        # Genereer rapport
        report = {
            'title': f'Rapport {period or "Alle data"}',
            'generated_at': datetime.now().isoformat(),
            'period': period or 'all_time',
            'total_logs': len(logs),
            'summary': self._generate_summary(logs),
            'insights': self._generate_insights(logs),
            'recommendations': self._generate_recommendations(logs)
        }

        # Sla rapport op
        self._save_report(report)

        return {
            'success': True,
            'message': f'✅ Rapport aangemaakt voor {period or "alle data"}',
            'report': report
        }

    def _get_statistics(self, text):
        """Haal statistieken op"""
        period = self._extract_time_period(text)
        logs = db.get_customer_logs(self.customer_id, limit=10000)

        # Filter op periode
        if period:
            logs = [
                log for log in logs
                if self._is_in_period(log['timestamp'], period)
            ]

        stats = {
            'total': len(logs),
            'period': period or 'all_time',
            'unique_ips': len(set(log['ip_address'] for log in logs)),
            'avg_per_day': len(logs) / max(1, self._days_in_period(period)),
            'peak_hour': self._get_peak_hour(logs),
            'trend': self._calculate_trend(logs)
        }

        return {
            'success': True,
            'message': f'📊 Statistieken voor {period or "alle data"}',
            'stats': stats
        }

    def _show_trend(self, text):
        """Toon trend analyse"""
        period = self._extract_time_period(text) or 'afgelopen_maand'
        logs = db.get_customer_logs(self.customer_id, limit=10000)

        # Groepeer per dag
        daily_counts = defaultdict(int)
        for log in logs:
            date = log['timestamp'][:10]
            daily_counts[date] += 1

        trend_data = [
            {'date': date, 'count': count}
            for date, count in sorted(daily_counts.items())
        ]

        # Bereken trend richting
        if len(trend_data) > 1:
            first_half = sum(d['count'] for d in trend_data[:len(trend_data)//2])
            second_half = sum(d['count'] for d in trend_data[len(trend_data)//2:])
            direction = 'stijgend' if second_half > first_half else 'dalend'
        else:
            direction = 'stabiel'

        return {
            'success': True,
            'message': f'📈 Trend is {direction}',
            'trend': {
                'direction': direction,
                'data': trend_data,
                'period': period
            }
        }

    def _create_summary(self, text):
        """Maak samenvatting van data"""
        logs = db.get_customer_logs(self.customer_id, limit=100)

        # Analyseer meest voorkomende patterns
        data_patterns = defaultdict(int)
        for log in logs:
            try:
                data = json.loads(log['data'])
                for key in data.keys():
                    data_patterns[key] += 1
            except (json.JSONDecodeError, TypeError, KeyError):
                pass

        summary = {
            'total_logs': len(logs),
            'recent_activity': 'hoog' if len(logs) > 50 else 'normaal',
            'common_fields': dict(sorted(data_patterns.items(), key=lambda x: x[1], reverse=True)[:5]),
            'last_log': logs[0]['timestamp'] if logs else None
        }

        return {
            'success': True,
            'message': '📝 Samenvatting gegenereerd',
            'summary': summary
        }

    def _search_data(self, text):
        """Zoek in data"""
        # Extract zoekterm
        search_query = text.replace('zoek', '').replace('vind', '').strip()

        logs = db.search_logs(search_query, customer_id=self.customer_id)

        return {
            'success': True,
            'message': f'🔍 {len(logs)} resultaten gevonden voor "{search_query}"',
            'results': logs[:10]  # Top 10
        }

    def _set_reminder(self, text):
        """Zet reminder (future feature)"""
        return {
            'success': True,
            'message': '⏰ Reminder functie komt binnenkort beschikbaar',
            'note': 'Deze feature wordt binnenkort toegevoegd'
        }

    def _get_help(self):
        """Toon help voorbeelden"""
        examples = [
            "📊 Hoeveel logs waren er vandaag?",
            "📈 Laat trend zien van deze maand",
            "📝 Maak een rapport van afgelopen week",
            "🔍 Zoek naar 'container'",
            "📋 Geef me een samenvatting",
            "⏰ Herinner me morgen om rapport te checken"
        ]

        return {
            'success': True,
            'message': '💡 Dit kan ik voor je doen:',
            'examples': examples
        }

    # ══════════════════════════════════════════════════
    # PROACTIEVE SUGGESTIES
    # ══════════════════════════════════════════════════

    def get_proactive_suggestions(self):
        """
        Genereer proactieve suggesties gebaseerd op klant data

        Voorbeelden:
        - "Je hebt weinig activiteit deze week, check je systeem"
        - "Top 3 IPs genereren 80% van verkeer, overweeg whitelisting"
        - "Piek activiteit op dinsdag 14:00, plan onderhoud buiten deze tijd"
        """
        if not self.enabled or not self.preferences['proactive']:
            return []

        suggestions = []

        # Haal recente data op
        logs = db.get_customer_logs(self.customer_id, limit=1000)
        stats = db.get_customer_stats(self.customer_id)

        # Suggestie 1: Lage activiteit
        if stats['logs_today'] < stats['total_logs'] / max(1, stats['total_logs'] // 100):
            suggestions.append({
                'type': 'warning',
                'title': '⚠️ Lage Activiteit',
                'message': f'Vandaag slechts {stats["logs_today"]} logs, veel lager dan normaal',
                'action': 'Check je systeem connectie'
            })

        # Suggestie 2: Groeiende trend
        if len(logs) > 100:
            recent = logs[:50]
            older = logs[50:100]
            if len(recent) > len(older) * 1.5:
                suggestions.append({
                    'type': 'info',
                    'title': '📈 Groeiende Activiteit',
                    'message': 'Je activiteit groeit! +50% vergeleken met eerder',
                    'action': 'Overweeg capacity upgrade'
                })

        # Suggestie 3: Top IPs domineren
        if len(logs) > 20:
            ip_counts = defaultdict(int)
            for log in logs:
                ip_counts[log['ip_address']] += 1

            top_3_percentage = sum(sorted(ip_counts.values(), reverse=True)[:3]) / len(logs)
            if top_3_percentage > 0.8:
                suggestions.append({
                    'type': 'tip',
                    'title': '💡 IP Whitelist Suggestie',
                    'message': f'Top 3 IPs genereren {int(top_3_percentage*100)}% van verkeer',
                    'action': 'Overweeg deze IPs te whitelisten voor betere performance'
                })

        # Suggestie 4: Wekelijks rapport
        if datetime.now().weekday() == 4:  # Vrijdag
            suggestions.append({
                'type': 'reminder',
                'title': '📊 Wekelijks Rapport',
                'message': 'Het is vrijdag! Tijd voor je wekelijkse overzicht',
                'action': 'Vraag: "Maak een rapport van deze week"'
            })

        # Suggestie 5: Ongebruikte features
        api_keys = db.get_customer_api_keys(self.customer_id)
        if len(api_keys) == 0:
            suggestions.append({
                'type': 'feature',
                'title': '🔑 Probeer API Access',
                'message': 'Je gebruikt nog geen API keys voor programmatic access',
                'action': 'Maak een API key aan voor automation'
            })

        return suggestions

    # ══════════════════════════════════════════════════
    # LEER VAN GEDRAG
    # ══════════════════════════════════════════════════

    def learn_from_interaction(self, command, result, feedback=None):
        """
        Leer van gebruikersinteracties
        - Welke commando's gebruikt klant vaak?
        - Welke tijd van dag is klant actief?
        - Welke type data zoekt klant meestal?
        """
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ai_learning (
                    customer_id,
                    command,
                    result_type,
                    success,
                    feedback,
                    timestamp
                ) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                self.customer_id,
                command,
                result.get('type'),
                result.get('success', True),
                feedback
            ))

    def get_learned_preferences(self):
        """Haal geleerde voorkeuren op"""
        with db.get_db() as conn:
            cursor = conn.cursor()

            # Most used commands
            cursor.execute('''
                SELECT command, COUNT(*) as count
                FROM ai_learning
                WHERE customer_id = ?
                GROUP BY command
                ORDER BY count DESC
                LIMIT 5
            ''', (self.customer_id,))

            most_used = [
                {'command': row['command'], 'count': row['count']}
                for row in cursor.fetchall()
            ]

            # Preferred time of day
            cursor.execute('''
                SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
                FROM ai_learning
                WHERE customer_id = ?
                GROUP BY hour
                ORDER BY count DESC
                LIMIT 1
            ''', (self.customer_id,))

            peak_hour = cursor.fetchone()

            return {
                'most_used_commands': most_used,
                'peak_usage_hour': peak_hour['hour'] if peak_hour else None,
                'total_interactions': sum(cmd['count'] for cmd in most_used)
            }

    # ══════════════════════════════════════════════════
    # HELPER FUNCTIES
    # ══════════════════════════════════════════════════

    def _extract_time_period(self, text):
        """Extract tijdsperiode uit tekst"""
        if 'vandaag' in text or 'today' in text:
            return 'vandaag'
        elif 'gisteren' in text or 'yesterday' in text:
            return 'gisteren'
        elif 'deze week' in text or 'this week' in text:
            return 'deze_week'
        elif 'afgelopen week' in text or 'last week' in text:
            return 'afgelopen_week'
        elif 'deze maand' in text or 'this month' in text:
            return 'deze_maand'
        elif 'afgelopen maand' in text or 'last month' in text:
            return 'afgelopen_maand'
        return None

    def _is_in_period(self, timestamp, period):
        """Check of timestamp in periode valt"""
        log_date = datetime.strptime(timestamp[:10], '%Y-%m-%d')
        now = datetime.now()

        if period == 'vandaag':
            return log_date.date() == now.date()
        elif period == 'gisteren':
            return log_date.date() == (now - timedelta(days=1)).date()
        elif period == 'deze_week':
            return log_date >= now - timedelta(days=now.weekday())
        elif period == 'afgelopen_week':
            week_start = now - timedelta(days=now.weekday() + 7)
            week_end = week_start + timedelta(days=7)
            return week_start <= log_date <= week_end
        elif period == 'deze_maand':
            return log_date.month == now.month and log_date.year == now.year
        elif period == 'afgelopen_maand':
            last_month = now.replace(day=1) - timedelta(days=1)
            return log_date.month == last_month.month and log_date.year == last_month.year

        return True

    def _days_in_period(self, period):
        """Bereken aantal dagen in periode"""
        if period in ['vandaag', 'gisteren']:
            return 1
        elif 'week' in period:
            return 7
        elif 'maand' in period:
            return 30
        return 1

    def _get_peak_hour(self, logs):
        """Vind piek uur"""
        hours = defaultdict(int)
        for log in logs:
            hour = int(log['timestamp'][11:13])
            hours[hour] += 1

        if not hours:
            return None

        peak = max(hours.items(), key=lambda x: x[1])
        return f"{peak[0]}:00 ({peak[1]} logs)"

    def _calculate_trend(self, logs):
        """Bereken trend"""
        if len(logs) < 2:
            return 'stabiel'

        mid = len(logs) // 2
        first_half = len(logs[:mid])
        second_half = len(logs[mid:])

        if second_half > first_half * 1.2:
            return 'stijgend'
        elif second_half < first_half * 0.8:
            return 'dalend'
        return 'stabiel'

    def _generate_summary(self, logs):
        """Genereer samenvatting van logs"""
        if not logs:
            return "Geen data beschikbaar"

        return f"{len(logs)} logs geanalyseerd. Meest recente: {logs[0]['timestamp'][:16]}"

    def _generate_insights(self, logs):
        """Genereer inzichten"""
        insights = []

        if len(logs) > 100:
            insights.append("Hoge activiteit gedetecteerd")

        # Check voor unieke IPs
        unique_ips = len(set(log['ip_address'] for log in logs))
        if unique_ips < len(logs) * 0.1:
            insights.append(f"Verkeer komt van slechts {unique_ips} IPs - zeer geconcentreerd")

        return insights

    def _generate_recommendations(self, logs):
        """Genereer aanbevelingen"""
        recommendations = []

        if len(logs) > 1000:
            recommendations.append("Overweeg data archivering voor oudere logs")

        if len(set(log['ip_address'] for log in logs)) > 100:
            recommendations.append("Veel verschillende IPs - overweeg rate limiting")

        return recommendations

    def _save_report(self, report):
        """Sla rapport op in database"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ai_generated_reports (
                    customer_id,
                    title,
                    content,
                    generated_at
                ) VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                self.customer_id,
                report['title'],
                json.dumps(report)
            ))

    def _get_suggestions(self):
        """Geef commando suggesties"""
        return [
            "Probeer: 'Hoeveel logs vandaag?'",
            "Probeer: 'Maak rapport van deze week'",
            "Probeer: 'Laat trend zien'"
        ]

# ═══════════════════════════════════════════════════════
# GLOBAL AI FUNCTIONS
# ═══════════════════════════════════════════════════════

def get_assistant(customer_id):
    """Haal AI Assistant op voor klant"""
    return AIAssistant(customer_id)

def enable_assistant(customer_id):
    """Activeer AI Assistant voor klant"""
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE customers
            SET ai_assistant_enabled = 1
            WHERE id = ?
        ''', (customer_id,))

def disable_assistant(customer_id):
    """Deactiveer AI Assistant"""
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE customers
            SET ai_assistant_enabled = 0
            WHERE id = ?
        ''', (customer_id,))

if __name__ == '__main__':
    print("AI Assistant module loaded successfully")
