#!/usr/bin/env python3
"""
MVAI Connexx - Automated Backup Script
Maak automatische backups van de database met retention policy
"""
import os
import shutil
import sqlite3
from datetime import datetime, timedelta
import glob

DATABASE = 'mvai_connexx.db'
BACKUP_DIR = 'backups'
RETENTION_DAYS = 30  # Bewaar backups voor 30 dagen

def create_backup():
    """Maak database backup"""

    # Maak backup directory als het niet bestaat
    os.makedirs(BACKUP_DIR, exist_ok=True)

    # Timestamp voor backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f'mvai_connexx_{timestamp}.db')

    try:
        # SQLite online backup (werkt ook tijdens gebruik)
        source_conn = sqlite3.connect(DATABASE)
        backup_conn = sqlite3.connect(backup_file)

        with backup_conn:
            source_conn.backup(backup_conn)

        source_conn.close()
        backup_conn.close()

        print(f"✓ Backup created: {backup_file}")

        # Bereken bestandsgrootte
        size = os.path.getsize(backup_file)
        size_mb = size / (1024 * 1024)
        print(f"  Size: {size_mb:.2f} MB")

        return backup_file

    except Exception as e:
        print(f"✗ Backup failed: {e}")
        return None

def cleanup_old_backups():
    """Verwijder oude backups volgens retention policy"""

    cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)

    # Vind alle backup bestanden
    backup_files = glob.glob(os.path.join(BACKUP_DIR, 'mvai_connexx_*.db'))

    deleted_count = 0

    for backup_file in backup_files:
        # Parse timestamp uit filename
        filename = os.path.basename(backup_file)
        try:
            # Extract timestamp (mvai_connexx_20231227_143020.db)
            timestamp_str = filename.replace('mvai_connexx_', '').replace('.db', '')
            file_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')

            # Verwijder als ouder dan retention period
            if file_date < cutoff_date:
                os.remove(backup_file)
                deleted_count += 1
                print(f"✓ Deleted old backup: {filename}")

        except (ValueError, IndexError):
            # Skip files met verkeerde naam format
            continue

    if deleted_count > 0:
        print(f"✓ Cleaned up {deleted_count} old backups")
    else:
        print("✓ No old backups to clean")

def list_backups():
    """Toon alle beschikbare backups"""

    backup_files = sorted(glob.glob(os.path.join(BACKUP_DIR, 'mvai_connexx_*.db')), reverse=True)

    if not backup_files:
        print("No backups found")
        return

    print(f"\nAvailable backups ({len(backup_files)}):\n")

    for i, backup_file in enumerate(backup_files, 1):
        filename = os.path.basename(backup_file)
        size = os.path.getsize(backup_file) / (1024 * 1024)
        mtime = datetime.fromtimestamp(os.path.getmtime(backup_file))

        print(f"{i}. {filename}")
        print(f"   Size: {size:.2f} MB")
        print(f"   Created: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

def restore_backup(backup_file):
    """Restore database van backup"""

    if not os.path.exists(backup_file):
        print(f"✗ Backup niet gevonden: {backup_file}")
        return False

    try:
        # Maak eerst een backup van huidige database
        current_backup = f"{DATABASE}.pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(DATABASE, current_backup)
        print(f"✓ Current database backed up to: {current_backup}")

        # Restore van backup
        shutil.copy2(backup_file, DATABASE)
        print(f"✓ Database restored from: {backup_file}")

        return True

    except Exception as e:
        print(f"✗ Restore failed: {e}")
        return False

if __name__ == '__main__':
    import sys

    print("=" * 60)
    print("MVAI CONNEXX - DATABASE BACKUP UTILITY")
    print("=" * 60)
    print()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'list':
            list_backups()

        elif command == 'restore':
            if len(sys.argv) < 3:
                print("Usage: python backup.py restore <backup_file>")
                sys.exit(1)

            backup_file = sys.argv[2]
            restore_backup(backup_file)

        elif command == 'create':
            create_backup()
            cleanup_old_backups()

        else:
            print(f"Unknown command: {command}")
            print("Available commands: create, list, restore")

    else:
        # Default: create backup
        create_backup()
        cleanup_old_backups()

    print()
    print("=" * 60)
