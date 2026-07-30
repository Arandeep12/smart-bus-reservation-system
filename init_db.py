"""
==============================================================================
Normalized Database Schema & Initializer Script
Developed & Architected by ADS Studio (Arandeep Singh Studio)
==============================================================================
"""

import os
import sqlite3

DB_PATH = 'database.db'

def get_connection():
    """Create sqlite connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force=False):
    """
    Initialize normalized SQLite database schema.
    If force=True, removes existing database file.
    """
    if force and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = get_connection()
    c = conn.cursor()

    # 1. States & Union Territories Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL
        )
    ''')

    # 2. Districts Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS districts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            is_major BOOLEAN DEFAULT 0,
            FOREIGN KEY (state_id) REFERENCES states (id) ON DELETE CASCADE,
            UNIQUE (state_id, name)
        )
    ''')

    # 3. Routes Table (District to District)
    c.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_district_id INTEGER NOT NULL,
            destination_district_id INTEGER NOT NULL,
            distance_km REAL DEFAULT 350.0,
            estimated_duration_hrs REAL DEFAULT 7.5,
            FOREIGN KEY (source_district_id) REFERENCES districts (id) ON DELETE CASCADE,
            FOREIGN KEY (destination_district_id) REFERENCES districts (id) ON DELETE CASCADE,
            UNIQUE (source_district_id, destination_district_id)
        )
    ''')

    # 4. Buses Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT UNIQUE NOT NULL,
            route_id INTEGER NOT NULL,
            operator_name TEXT NOT NULL,
            bus_type TEXT NOT NULL,
            seat_layout TEXT NOT NULL DEFAULT '2x2',
            total_seats INTEGER NOT NULL DEFAULT 40,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            price REAL NOT NULL,
            rating REAL DEFAULT 4.5,
            amenities TEXT,
            FOREIGN KEY (route_id) REFERENCES routes (id) ON DELETE CASCADE
        )
    ''')

    # 5. Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            email TEXT
        )
    ''')

    # 6. Bookings Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_ref TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            bus_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            seat_numbers TEXT NOT NULL,
            passengers_count INTEGER DEFAULT 1,
            total_price REAL NOT NULL,
            payment_status TEXT DEFAULT 'PAID',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (bus_id) REFERENCES buses (id) ON DELETE CASCADE
        )
    ''')

    # 7. Seats Table (Date & Bus specific reservations)
    c.execute('''
        CREATE TABLE IF NOT EXISTS seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            seat_number TEXT NOT NULL,
            is_booked BOOLEAN DEFAULT 0,
            FOREIGN KEY (bus_id) REFERENCES buses (id) ON DELETE CASCADE,
            UNIQUE (bus_id, date, seat_number)
        )
    ''')

    # Performance Indexes
    c.execute("CREATE INDEX IF NOT EXISTS idx_districts_state ON districts(state_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_routes_src_dest ON routes(source_district_id, destination_district_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_buses_route ON buses(route_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_seats_bus_date ON seats(bus_id, date, seat_number)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_bookings_ref ON bookings(booking_ref)")

    conn.commit()

    # Check if database needs seeding
    c.execute("SELECT COUNT(*) FROM districts")
    districts_count = c.fetchone()[0]

    conn.close()

    if districts_count == 0:
        print("Database schema created. Triggering database seed engine...")
        from seed_db import seed_db
        seed_db()
    else:
        print("Database schema verified.")

def ensure_db_exists():
    """Ensure database schema and initial seed exist on startup."""
    if not os.path.exists(DB_PATH):
        init_db(force=True)
    else:
        init_db(force=False)

if __name__ == '__main__':
    init_db(force=True)
