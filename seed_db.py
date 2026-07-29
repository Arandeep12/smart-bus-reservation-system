import sqlite3
import random

INDIAN_STATES = [
    # 28 States
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    # 8 Union Territories
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

BUS_TYPES = ["AC", "Non-AC", "Sleeper"]

def generate_time_pair():
    dep_hour = random.randint(0, 23)
    dep_min = random.choice(["00", "15", "30", "45"])
    
    # Duration between 4 to 16 hours
    duration = random.randint(4, 16)
    arr_hour = (dep_hour + duration) % 24
    arr_min = random.choice(["00", "15", "30", "45"])
    
    return f"{dep_hour:02d}:{dep_min}", f"{arr_hour:02d}:{arr_min}"

def seed_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Clear existing routes, buses, seats, bookings
    c.execute("DELETE FROM seats")
    c.execute("DELETE FROM bookings")
    c.execute("DELETE FROM buses")
    c.execute("DELETE FROM routes")
    
    # reset autoincrement
    c.execute("DELETE FROM sqlite_sequence WHERE name='seats'")
    c.execute("DELETE FROM sqlite_sequence WHERE name='bookings'")
    c.execute("DELETE FROM sqlite_sequence WHERE name='buses'")
    c.execute("DELETE FROM sqlite_sequence WHERE name='routes'")

    print("Generating routes and buses...")
    
    route_id = 1
    for source in INDIAN_STATES:
        for destination in INDIAN_STATES:
            if source == destination:
                continue
            
            c.execute("INSERT INTO routes (source, destination) VALUES (?, ?)", (source, destination))
            
            # Create 3-5 buses for each route
            num_buses = random.randint(3, 5)
            for i in range(num_buses):
                bus_type = random.choice(BUS_TYPES)
                total_seats = 30 if bus_type == "Sleeper" else (40 if bus_type == "AC" else 50)
                price = random.randint(500, 2500) if bus_type == "AC" or bus_type == "Sleeper" else random.randint(300, 1000)
                dep_time, arr_time = generate_time_pair()
                
                # generate a bus number like DEL-BOM-1234
                prefix1 = source[:3].upper()
                prefix2 = destination[:3].upper()
                bus_num = f"{prefix1}-{prefix2}-{random.randint(1000, 9999)}"
                
                c.execute('''
                    INSERT INTO buses (bus_number, route_id, bus_type, total_seats, departure_time, arrival_time, price) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (bus_num, route_id, bus_type, total_seats, dep_time, arr_time, price))
            
            route_id += 1

    conn.commit()
    conn.close()
    print("Database seeded with buses for all 1260 route combinations!")

if __name__ == '__main__':
    seed_db()
