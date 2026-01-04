"""
MVAI Connexx - Email Notification System
Simpel, effectief, sales-ready
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config

class EmailService:
    """Send emails via SMTP - Production ready"""

    def __init__(self):
        self.smtp_server = config.Config.SMTP_SERVER
        self.smtp_port = config.Config.SMTP_PORT
        self.smtp_username = config.Config.SMTP_USERNAME
        self.smtp_password = config.Config.SMTP_PASSWORD
        self.from_email = config.Config.SMTP_FROM_EMAIL
        self.from_name = config.Config.SMTP_FROM_NAME

    def _send_email(self, to_email: str, subject: str, body_html: str, body_text: str = None):
        """Internal: Send email via SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            # Text fallback
            if body_text:
                part1 = MIMEText(body_text, 'plain')
                msg.attach(part1)

            # HTML version
            part2 = MIMEText(body_html, 'html')
            msg.attach(part2)

            # Send via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            return True

        except Exception as e:
            print(f"❌ Email error: {e}")
            return False

    def send_welcome_email(self, customer_name: str, customer_email: str, access_code: str):
        """Welkom email bij nieuwe customer"""
        subject = f"Welkom bij MVAI Connexx, {customer_name}!"

        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #00ff41 0%, #00dd35 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">🎉 Welkom bij MVAI Connexx!</h1>
            </div>

            <div style="padding: 30px; background: #f5f5f5;">
                <h2 style="color: #333;">Hallo {customer_name},</h2>

                <p style="font-size: 16px; color: #666;">
                    Je account is succesvol aangemaakt! Je kunt nu direct aan de slag met ons enterprise platform.
                </p>

                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">📧 Jouw Login Gegevens:</h3>
                    <p><strong>Access Code:</strong> <code style="background: #f0f0f0; padding: 5px 10px; border-radius: 4px; font-size: 18px;">{access_code}</code></p>
                    <p><strong>Login URL:</strong> <a href="https://mindvault-ai.com/login">https://mindvault-ai.com/login</a></p>
                </div>

                <div style="background: #e8f5e9; padding: 15px; border-left: 4px solid #00ff41; margin: 20px 0;">
                    <p style="margin: 0;"><strong>💡 Pro Tip:</strong> Bewaar je access code veilig! Je hebt deze nodig om in te loggen.</p>
                </div>

                <h3>🚀 Wat kun je nu doen?</h3>
                <ul style="color: #666;">
                    <li>Login op het platform</li>
                    <li>Bekijk je dashboard met real-time analytics</li>
                    <li>Start met data logging via API of UI</li>
                    <li>Genereer je eerste API keys</li>
                    <li>Exporteer data naar CSV</li>
                </ul>

                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://mindvault-ai.com/login"
                       style="background: #00ff41; color: #000; padding: 15px 40px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                        🔐 Inloggen
                    </a>
                </div>

                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

                <p style="color: #999; font-size: 14px;">
                    <strong>Hulp nodig?</strong><br>
                    📧 Email: <a href="mailto:info@mindvault-ai.com">info@mindvault-ai.com</a><br>
                    🌐 Website: <a href="https://mindvault-ai.com">mindvault-ai.com</a>
                </p>

                <p style="color: #999; font-size: 12px; text-align: center;">
                    © {datetime.now().year} Mind Vault AI | Enterprise Multi-Tenant Platform<br>
                    99.9% SLA Guarantee | ISO-Certified Security
                </p>
            </div>
        </body>
        </html>
        """

        body_text = f"""
        Welkom bij MVAI Connexx!

        Hallo {customer_name},

        Je account is succesvol aangemaakt!

        Access Code: {access_code}
        Login URL: https://mindvault-ai.com/login

        Bewaar je access code veilig!

        Hulp nodig? Email: info@mindvault-ai.com

        © {datetime.now().year} Mind Vault AI
        """

        return self._send_email(customer_email, subject, body_html, body_text)

    def send_tier_upgrade_email(self, customer_name: str, customer_email: str, old_tier: str, new_tier: str, new_price: float):
        """Email bij tier upgrade"""
        subject = f"🎊 Je bent geüpgraded naar {new_tier.upper()}!"

        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #00ff41 0%, #00dd35 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">🚀 Upgrade Succesvol!</h1>
            </div>

            <div style="padding: 30px; background: #f5f5f5;">
                <h2 style="color: #333;">Gefeliciteerd, {customer_name}!</h2>

                <p style="font-size: 16px; color: #666;">
                    Je bent succesvol geüpgraded van <strong>{old_tier}</strong> naar <strong>{new_tier}</strong>!
                </p>

                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">📊 Nieuw Abonnement:</h3>
                    <p><strong>Tier:</strong> {new_tier.upper()}</p>
                    <p><strong>Prijs:</strong> €{new_price:.2f}/maand</p>
                    <p><strong>Ingangsdatum:</strong> {datetime.now().strftime('%d-%m-%Y')}</p>
                </div>

                <h3>✨ Je hebt nu toegang tot:</h3>
                <ul style="color: #666;">
                    <li>Meer logs per maand</li>
                    <li>Geavanceerde analytics</li>
                    <li>Priority support</li>
                    <li>API rate limit verhoogd</li>
                    <li>Enterprise dashboards</li>
                </ul>

                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://mindvault-ai.com/dashboard"
                       style="background: #00ff41; color: #000; padding: 15px 40px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                        📊 Bekijk Dashboard
                    </a>
                </div>

                <p style="color: #999; font-size: 14px;">
                    <strong>Vragen?</strong> Email ons: <a href="mailto:info@mindvault-ai.com">info@mindvault-ai.com</a>
                </p>
            </div>
        </body>
        </html>
        """

        body_text = f"""
        Upgrade Succesvol!

        Gefeliciteerd {customer_name},

        Je bent geüpgraded van {old_tier} naar {new_tier}!

        Nieuw abonnement: €{new_price:.2f}/maand
        Ingangsdatum: {datetime.now().strftime('%d-%m-%Y')}

        Login: https://mindvault-ai.com/dashboard

        © {datetime.now().year} Mind Vault AI
        """

        return self._send_email(customer_email, subject, body_html, body_text)

    def send_admin_alert(self, alert_type: str, message: str, severity: str = "HIGH"):
        """Email naar admin bij kritieke events"""
        subject = f"🚨 ALERT [{severity}]: {alert_type}"

        body_html = f"""
        <html>
        <body style="font-family: monospace; max-width: 600px; margin: 0 auto;">
            <div style="background: {'#ff4444' if severity == 'CRITICAL' else '#ff9800'}; padding: 20px; color: white;">
                <h2 style="margin: 0;">🚨 MVAI Connexx Alert</h2>
            </div>

            <div style="padding: 20px; background: #f5f5f5;">
                <p><strong>Type:</strong> {alert_type}</p>
                <p><strong>Severity:</strong> {severity}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

                <div style="background: white; padding: 15px; margin: 20px 0; border-left: 4px solid #ff4444;">
                    <pre style="margin: 0;">{message}</pre>
                </div>

                <p style="font-size: 12px; color: #999;">
                    This is an automated alert from MVAI Connexx monitoring system.
                </p>
            </div>
        </body>
        </html>
        """

        # Send to admin email
        admin_email = config.Config.COMPANY_EMAIL
        return self._send_email(admin_email, subject, body_html)

    def send_usage_limit_warning(self, customer_name: str, customer_email: str, current_usage: int, limit: int, tier: str):
        """Waarschuwing bij 80% usage"""
        percentage = (current_usage / limit) * 100

        subject = f"⚠️ Je bereikt je maandelijkse limiet ({percentage:.0f}%)"

        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #ff9800; padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">⚠️ Usage Waarschuwing</h1>
            </div>

            <div style="padding: 30px; background: #f5f5f5;">
                <h2 style="color: #333;">Hallo {customer_name},</h2>

                <p style="font-size: 16px; color: #666;">
                    Je hebt <strong>{percentage:.0f}%</strong> van je maandelijkse log limiet gebruikt.
                </p>

                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Huidig Tier:</strong> {tier.upper()}</p>
                    <p><strong>Gebruikt:</strong> {current_usage:,} / {limit:,} logs</p>
                    <p><strong>Resterende:</strong> {limit - current_usage:,} logs</p>
                </div>

                <div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ff9800; margin: 20px 0;">
                    <p style="margin: 0;"><strong>💡 Wat gebeurt er bij 100%?</strong><br>
                    Je kunt nog steeds data loggen, maar we raden een upgrade aan voor optimale performance.</p>
                </div>

                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://mindvault-ai.com/customer/subscription"
                       style="background: #00ff41; color: #000; padding: 15px 40px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                        🚀 Upgrade Nu
                    </a>
                </div>
            </div>
        </body>
        </html>
        """

        return self._send_email(customer_email, subject, body_html)


# Convenience functions
email_service = EmailService()

def send_welcome_email(customer_name, customer_email, access_code):
    """Send welkom email - direct te gebruiken"""
    return email_service.send_welcome_email(customer_name, customer_email, access_code)

def send_tier_upgrade_email(customer_name, customer_email, old_tier, new_tier, new_price):
    """Send upgrade email"""
    return email_service.send_tier_upgrade_email(customer_name, customer_email, old_tier, new_tier, new_price)

def send_admin_alert(alert_type, message, severity="HIGH"):
    """Send admin alert"""
    return email_service.send_admin_alert(alert_type, message, severity)

def send_usage_limit_warning(customer_name, customer_email, current_usage, limit, tier):
    """Send usage warning"""
    return email_service.send_usage_limit_warning(customer_name, customer_email, current_usage, limit, tier)
