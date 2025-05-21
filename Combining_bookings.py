import requests
import sqlite3
import json
from datetime import datetime, timedelta

# === Configuration ===

# Cloudbeds
CLOUDBEDS_TOKEN = "deleted in github for privacy :)"
CLOUDBEDS_BASE_URL = "https://hotels.cloudbeds.com/api/v1.1"

# Lodgify
LODGIFY_API_KEY = "YOUR_LODGIFY_API_KEY"
LODGIFY_BASE_URL = "deleted in github for privacy :)"

# Database
DB_FILE = "combined_bookings.db"

# === Initialize SQLite Database ===
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id TEXT PRIMARY KEY,
            source TEXT,
            guest_name TEXT,
            check_in TEXT,
            check_out TEXT,
            total_price REAL,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

# === Fetch Bookings from Cloudbeds ===
def fetch_cloudbeds_bookings():
    url = f"{CLOUDBEDS_BASE_URL}/getReservations"
    headers = {"Authorization": f"Bearer {CLOUDBEDS_TOKEN}"}
    today = datetime.utcnow().strftime('%Y-%m-%d')
    params = {
        "start_date": today,
        "end_date": today
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    bookings = response.json().get('data', [])
    result = []
    for b in bookings:
        result.append({
            "id": f"cloudbeds_{b['reservationID']}",
            "source": "Cloudbeds",
            "guest_name": f"{b.get('guest', {}).get('firstName', '')} {b.get('guest', {}).get('lastName', '')}",
            "check_in": b.get('checkIn'),
            "check_out": b.get('checkOut'),
            "total_price": float(b.get('total', 0)),
            "created_at": b.get('created')
        })
    return result

# === Fetch Bookings from Lodgify ===
def fetch_lodgify_bookings():
    url = f"{LODGIFY_BASE_URL}/reservations"
    headers = {
        "x-api-key": LODGIFY_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    bookings = response.json().get('reservations', [])
    result = []
    for b in bookings:
        result.append({
            "id": f"lodgify_{b['id']}",
            "source": "Lodgify",
            "guest_name": b.get('guestName'),
            "check_in": b.get('checkInDate'),
            "check_out": b.get('checkOutDate'),
            "total_price": float(b.get('totalPrice', 0)),
            "created_at": b.get('createdAt')
        })
    return result

# === Store Combined Bookings in SQLite ===
def store_bookings(bookings):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for b in bookings:
        try:
            c.execute("""
                INSERT INTO bookings (id, source, guest_name, check_in, check_out, total_price, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                b['id'],
                b['source'],
                b['guest_name'],
                b['check_in'],
                b['check_out'],
                b['total_price'],
                b['created_at']
            ))
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate booking: {b['id']}")
    conn.commit()
    conn.close()

# === Main ===
def main():
    print("Initializing database...")
    init_db()

    print("Fetching bookings from Cloudbeds...")
    cb_bookings = fetch_cloudbeds_bookings()

    print("Fetching bookings from Lodgify...")
    lodgify_bookings = fetch_lodgify_bookings()

    combined = cb_bookings + lodgify_bookings
    print(f"Total new bookings to store: {len(combined)}")

    store_bookings(combined)
    print("All new bookings stored.")

if __name__ == "__main__":
    main()
