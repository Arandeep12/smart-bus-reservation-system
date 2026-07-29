"""
==============================================================================
Database Schema & Initializer Script
Developed & Architected by ADS Studio (Arandeep Singh Studio)
==============================================================================
"""

import os
import sqlite3

DB_PATH = 'database.db'

def init_db(force=False):
    """
    Initialize SQLite database schema and seed initial sample routes/buses.
    If force=True, removes existing database file.
    """
    if force and os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create Users Table
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

    # Create Routes Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            destination TEXT NOT NULL
        )
    ''')

    # Create Buses Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT NOT NULL,
            route_id INTEGER,
            bus_type TEXT,
            total_seats INTEGER,
            departure_time TEXT,
            arrival_time TEXT,
            price REAL,
            FOREIGN KEY (route_id) REFERENCES routes (id)
        )
    ''')

    # Create Seats Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_id INTEGER,
            date TEXT,
            seat_number TEXT,
            is_booked BOOLEAN DEFAULT 0,
            FOREIGN KEY (bus_id) REFERENCES buses (id)
        )
    ''')

    # Create Bookings Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_ref TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            bus_id INTEGER,
            date TEXT,
            seat_numbers TEXT,
            total_price REAL,
            payment_status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (bus_id) REFERENCES buses (id)
        )
    ''')

    # Insert default sample data if routes table is empty
    c.execute("SELECT COUNT(*) FROM routes")
    if c.fetchone()[0] == 0:
        # Default Indian Interstate Routes
        routes_data = [
            ('Delhi', 'Maharashtra'),
            ('Karnataka', 'Tamil Nadu'),
            ('Telangana', 'Andhra Pradesh'),
            ('Gujarat', 'Rajasthan'),
            ('West Bengal', 'Odisha'),
            ('Uttar Pradesh', 'Bihar'),
            ('Punjab', 'Haryana'),
            ('Kerala', 'Karnataka')
        ]
        for src, dest in routes_data:
            c.execute("INSERT INTO routes (source, destination) VALUES (?, ?)", (src, dest))

        # Default Buses
        buses_data = [
            # Delhi -> Maharashtra (Route ID 1)
            ('DEL-BOM-001', 1, 'AC', 40, '08:00', '22:00', 1500.00),
            ('DEL-BOM-002', 1, 'Sleeper', 30, '18:00', '08:00', 2500.00),
            # Karnataka -> Tamil Nadu (Route ID 2)
            ('BLR-CHN-001', 2, 'Non-AC', 50, '06:00', '13:00', 600.00),
            ('BLR-CHN-002', 2, 'AC', 40, '14:00', '20:30', 950.00),
            # Telangana -> Andhra Pradesh (Route ID 3)
            ('HYD-VZG-001', 3, 'Sleeper', 30, '20:00', '06:00', 1200.00)
        ]
        for bus_num, route_id, btype, seats, dept, arr, price in buses_data:
            c.execute(
                "INSERT INTO buses (bus_number, route_id, bus_type, total_seats, departure_time, arrival_time, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (bus_num, route_id, btype, seats, dept, arr, price)
            )

    conn.commit()
    conn.close()
    print("Database initialization complete.")

def ensure_db_exists():
    """Ensure database file and schema exist on startup."""
    init_db(force=False)

if __name__ == '__main__':
    init_db(force=True)
