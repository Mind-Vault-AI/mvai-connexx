"""
MVAI Connexx - Demo Data Seeding
Maak demo klanten met fictieve data voor presentatie
"""
import random
from datetime import datetime, timedelta
import database as db

# Fictieve bedrijven voor demo
DEMO_COMPANIES = [
    {
        "name": "TransLog Nederland BV",
        "email": "info@translog.nl",
        "info": "Logistiek dienstverlener gespecialiseerd in warehousing en transport"
    },
    {
        "name": "VanderMeer Logistics",
        "email": "contact@vandermeer-logistics.nl",
        "info": "Full-service logistieke partner voor automotive industry"
    },
    {
        "name": "SmartChain Solutions",
        "email": "hello@smartchain.nl",
        "info": "Supply chain optimalisatie met AI-gedreven oplossingen"
    },
    {
        "name": "Rotterdam Cargo Services",
        "email": "support@rotterdamcargo.nl",
        "info": "Haven-gebonden logistiek en cargo handling"
    },
    {
        "name": "EcoFreight Europe",
        "email": "info@ecofreight.eu",
        "info": "Duurzame transport oplossingen voor Europa-breed vervoer"
    }
]

# Fictieve log entries voor realistische data
DEMO_LOG_TEMPLATES = [
    "Container #CONT-{n} gearriveerd op locatie {loc}. Status: OK. Temperatuur: {temp}°C",
    "Pallet {n} verzonden naar klant {customer}. Verwachte levering: {date}",
    "Kwaliteitscontrole uitgevoerd op zending {n}. Resultaat: {result}",
    "Track & Trace update: Order #{n} is {status}. ETA: {time}",
    "Inventaris telling locatie {loc}: {n} units geteld. Delta: {delta}",
    "Loading dock {n} bezet. Laadtijd: {time} minuten. Efficiency: {eff}%",
    "Route optimalisatie: Rit {n} bespaart {saving} km via nieuwe route",
    "Veiligheidscheck voertuig {n}: {result}. Volgende check: {date}",
]

def generate_demo_logs(customer_id, count=15):
    """Genereer fictieve logs voor een klant"""
    locations = ["Amsterdam", "Rotterdam", "Utrecht", "Eindhoven", "Venlo"]
    customers = ["ACME Corp", "GlobalTech", "EuroRetail", "MegaMart", "FastShip"]
    statuses = ["onderweg", "afgeleverd", "in behandeling", "gereed voor verzending"]
    results = ["GOEDGEKEURD", "GOEDGEKEURD", "GOEDGEKEURD", "AFKEUR - HERCONTROLE"]

    logs = []

    for i in range(count):
        # Random timestamp in afgelopen 30 dagen
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago)

        # Kies random template
        template = random.choice(DEMO_LOG_TEMPLATES)

        # Vul template met random data
        data = template.format(
            n=random.randint(1000, 9999),
            loc=random.choice(locations),
            temp=random.randint(2, 8),
            customer=random.choice(customers),
            date=(datetime.now() + timedelta(days=random.randint(1, 5))).strftime("%d-%m-%Y"),
            result=random.choice(results),
            status=random.choice(statuses),
            time=random.randint(15, 90),
            delta=random.randint(-5, 5),
            eff=random.randint(75, 98),
            saving=random.randint(5, 50)
        )

        # Random IP adressen
        ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"

        logs.append({
            'customer_id': customer_id,
            'ip_address': ip,
            'data': data,
            'timestamp': timestamp
        })

    # Sorteer op tijd (oudste eerst)
    logs.sort(key=lambda x: x['timestamp'])

    return logs

def seed_demo_data():
    """Seed database met demo data"""

    print("=" * 60)
    print("MVAI CONNEXX - DEMO DATA SEEDING")
    print("=" * 60)
    print()

    # Initialiseer database
    print("1. Initialiseren database...")
    db.init_db()
    print("   ✓ Database klaar")
    print()

    # Maak admin gebruiker aan
    print("2. Maken admin gebruiker...")
    admin = db.create_admin("admin", "admin123")  # Simpel wachtwoord voor demo
    print(f"   ✓ Admin aangemaakt")
    print(f"   Username: {admin['username']}")
    print(f"   Access Code: {admin['access_code']}")
    print()

    # Maak demo klanten aan
    print("3. Maken demo klanten...")
    customers = []

    for i, company in enumerate(DEMO_COMPANIES, 1):
        customer = db.create_customer(
            name=company['name'],
            contact_email=company['email'],
            company_info=company['info']
        )
        customers.append(customer)
        print(f"   [{i}/{len(DEMO_COMPANIES)}] {company['name']}")
        print(f"       Access Code: {customer['access_code']}")

    print()
    print(f"   ✓ {len(customers)} klanten aangemaakt")
    print()

    # Genereer logs voor elke klant
    print("4. Genereren demo logs...")
    total_logs = 0

    for i, customer in enumerate(customers, 1):
        # Varieer aantal logs per klant (10-25)
        log_count = random.randint(10, 25)
        logs = generate_demo_logs(customer['id'], log_count)

        # Sla logs op
        for log in logs:
            db.create_log(
                customer_id=log['customer_id'],
                ip_address=log['ip_address'],
                data=log['data'],
                metadata=None
            )

        total_logs += len(logs)
        print(f"   [{i}/{len(customers)}] {customer['name']}: {len(logs)} logs")

    print()
    print(f"   ✓ {total_logs} logs gegenereerd")
    print()

    # Print samenvatting
    print("=" * 60)
    print("DEMO DATA SEEDING VOLTOOID!")
    print("=" * 60)
    print()
    print("LOGIN CREDENTIALS:")
    print()
    print("ADMIN:")
    print(f"  Access Code: {admin['access_code']}")
    print()
    print("KLANTEN:")
    for customer in customers:
        print(f"  {customer['name']}")
        print(f"    Access Code: {customer['access_code']}")
        print()

    print("=" * 60)
    print()
    print("Start de applicatie met: python app.py")
    print("Open je browser op: http://localhost:5000")
    print()

if __name__ == '__main__':
    seed_demo_data()
