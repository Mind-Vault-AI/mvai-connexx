"""
MVAI Connexx - Migration Script
Migreer JSON data naar SQLite database
"""
import json
import os
from datetime import datetime
import database as db

def migrate_json_to_sqlite():
    """Migreer bestaande JSON data naar SQLite database"""

    print("=" * 60)
    print("MVAI CONNEXX - DATABASE MIGRATIE")
    print("=" * 60)
    print()

    # Initialiseer database
    print("1. Initialiseren database...")
    db.init_db()
    print("   ✓ Database tabellen aangemaakt")
    print()

    # Check of JSON file bestaat
    json_file = 'mvai_data.json'
    if not os.path.exists(json_file):
        print(f"⚠ Geen bestaande data gevonden ({json_file})")
        print("   Starten met lege database.")
        return

    # Laad JSON data
    print("2. Laden JSON data...")
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"   ✗ Fout bij laden JSON: {e}")
        return

    logs = data.get('logs', [])
    print(f"   ✓ {len(logs)} logs gevonden in JSON")
    print()

    if not logs:
        print("   Geen logs om te migreren.")
        return

    # Maak default customer aan voor legacy data
    print("3. Maken default klant voor legacy data...")
    try:
        legacy_customer = db.create_customer(
            name="Legacy Data",
            contact_email="legacy@mvai.local",
            company_info="Automatisch gemigreerd van JSON data"
        )
        print(f"   ✓ Legacy klant aangemaakt (ID: {legacy_customer['id']})")
        print(f"   Access Code: {legacy_customer['access_code']}")
        print()
    except Exception as e:
        print(f"   ✗ Fout bij aanmaken klant: {e}")
        return

    # Migreer logs
    print("4. Migreren logs naar database...")
    migrated = 0
    failed = 0

    for log in logs:
        try:
            # Haal data op uit log
            ip_address = log.get('ip', 'unknown')
            timestamp = log.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # Maak data string (alle velden behalve ip en timestamp)
            log_data = {k: v for k, v in log.items() if k not in ['ip', 'timestamp']}
            data_str = json.dumps(log_data)

            # Maak log entry
            db.create_log(
                customer_id=legacy_customer['id'],
                ip_address=ip_address,
                data=data_str,
                metadata=None
            )

            migrated += 1
            if migrated % 10 == 0:
                print(f"   Gemigreerd: {migrated}/{len(logs)}")

        except Exception as e:
            failed += 1
            print(f"   ✗ Fout bij migreren log: {e}")

    print()
    print(f"   ✓ Migratie voltooid!")
    print(f"   - Succesvol: {migrated}")
    print(f"   - Gefaald: {failed}")
    print()

    # Backup oude JSON
    backup_file = f'mvai_data.json.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    try:
        os.rename(json_file, backup_file)
        print(f"5. JSON backup aangemaakt: {backup_file}")
    except Exception as e:
        print(f"   ⚠ Kon geen backup maken: {e}")

    print()
    print("=" * 60)
    print("MIGRATIE SUCCESVOL VOLTOOID!")
    print("=" * 60)
    print()
    print(f"Legacy Access Code: {legacy_customer['access_code']}")
    print()
    print("Je kunt nu de applicatie starten met: python app.py")
    print()

if __name__ == '__main__':
    migrate_json_to_sqlite()
