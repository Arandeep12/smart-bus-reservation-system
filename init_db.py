import sqlite3
import os

def init_db():
    if os.path.exists('database.db'):
        os.remove('database.db')
        
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

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

    c.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            destination TEXT NOT NULL
        )
    ''')

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

    # Add mock data - Indian Routes
    c.execute("INSERT INTO routes (source, destination) VALUES ('Delhi', 'Maharashtra')")
    c.execute("INSERT INTO routes (source, destination) VALUES ('Karnataka', 'Tamil Nadu')")
    c.execute("INSERT INTO routes (source, destination) VALUES ('Telangana', 'Andhra Pradesh')")
    c.execute("INSERT INTO routes (source, destination) VALUES ('Gujarat', 'Rajasthan')")
    c.execute("INSERT INTO routes (source, destination) VALUES ('West Bengal', 'Odisha')")
    c.execute("INSERT INTO routes (source, destination) VALUES ('Uttar Pradesh', 'Bihar')")
    c.execute("INSERT INTO routes (source, destination) VALUES ('Punjab', 'Haryana')")
    c.execute("INSERT INTO routes (source, destination) VALUES ('Kerala', 'Karnataka')")
    
    # Delhi -> Maharashtra Route ID 1
    c.execute("INSERT INTO buses (bus_number, route_id, bus_type, total_seats, departure_time, arrival_time, price) VALUES ('DEL-BOM-001', 1, 'AC', 40, '08:00', '22:00', 1500.00)")
    c.execute("INSERT INTO buses (bus_number, route_id, bus_type, total_seats, departure_time, arrival_time, price) VALUES ('DEL-BOM-002', 1, 'Sleeper', 30, '18:00', '08:00', 2500.00)")

    # Karnataka -> Tamil Nadu Route ID 2
    c.execute("INSERT INTO buses (bus_number, route_id, bus_type, total_seats, departure_time, arrival_time, price) VALUES ('BLR-CHN-001', 2, 'Non-AC', 50, '06:00', '13:00', 600.00)")
    c.execute("INSERT INTO buses (bus_number, route_id, bus_type, total_seats, departure_time, arrival_time, price) VALUES ('BLR-CHN-002', 2, 'AC', 40, '14:00', '20:30', 950.00)")

    # Telangana -> Andhra Pradesh Route ID 3
    c.execute("INSERT INTO buses (bus_number, route_id, bus_type, total_seats, departure_time, arrival_time, price) VALUES ('HYD-VZG-001', 3, 'Sleeper', 30, '20:00', '06:00', 1200.00)")

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
