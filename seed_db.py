"""
==============================================================================
High-Performance Database Seeding Engine
Populates 28 States, 8 UTs, 787 Districts, and Hundreds of Transport Routes
Developed & Architected by ADS Studio (Arandeep Singh Studio)
==============================================================================
"""

import sqlite3
import random
from india_locations import INDIA_LOCATIONS

DB_PATH = 'database.db'

OPERATORS = [
    "ADS Express", "KSRTC Swift", "MSRTC Shivneri", "UPSRTC Janrath",
    "Zingbus Premium", "IntrCity SmartBus", "VRL Travels", "SRS Travels",
    "Orange Tours & Travels", "Hans Travels", "Mahalaxmi Travels", "Raj National Express",
    "Shrinath Travels", "NueGo Electric AC", "InterCity Volvo Line", "Crown Travels"
]

BUS_TYPES = [
    {"type": "Volvo Multi-Axle AC (2+2)", "layout": "2x2", "seats": 40, "base_multiplier": 1.5, "amenities": "WiFi, Charging, Water, Blanket, Live Tracking"},
    {"type": "AC Sleeper (2+1)", "layout": "2x1", "seats": 30, "base_multiplier": 1.8, "amenities": "Personal TV, Charging, Pillow, Blanket, Reading Light"},
    {"type": "Luxury Semi-Sleeper AC (2+2)", "layout": "2x2", "seats": 44, "base_multiplier": 1.3, "amenities": "WiFi, Charging, Water Bottle, Reclining Seats"},
    {"type": "Non-AC Seater (2+2)", "layout": "2x2", "seats": 48, "base_multiplier": 0.9, "amenities": "Charging Port, Emergency Button"},
    {"type": "Non-AC Sleeper (2+1)", "layout": "2x1", "seats": 30, "base_multiplier": 1.1, "amenities": "Personal Curtain, Pillow, Reading Light"}
]

MAJOR_DISTRICT_NAMES = {
    # Major Hubs for inter-state & intra-state connectivity
    "Patna", "Muzaffarpur", "Gaya", "Raipur", "Durg", "Bilaspur", "North Goa", "South Goa",
    "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gurugram", "Faridabad", "Ambala", "Shimla",
    "Dharamshala", "Ranchi", "Dhanbad", "Jamshedpur", "Bengaluru Urban", "Mysuru", "Mangaluru",
    "Thiruvananthapuram", "Ernakulam", "Kozhikode", "Bhopal", "Indore", "Gwalior", "Jabalpur",
    "Mumbai City", "Pune", "Nagpur", "Nashik", "Aurangabad (Chhatrapati Sambhajinagar)",
    "Bhubaneswar", "Cuttack", "Rourkela", "Amritsar", "Ludhiana", "Jalandhar", "Patiala",
    "Jaipur", "Jodhpur", "Udaipur", "Kota", "Chennai", "Coimbatore", "Madurai", "Salem",
    "Hyderabad", "Warangal", "Agra", "Lucknow", "Varanasi", "Kanpur Nagar", "Prayagraj (Allahabad)",
    "Ghaziabad", "Noida", "Dehradun", "Haridwar", "Kolkata", "Howrah", "Siliguri",
    "New Delhi", "Central Delhi", "Chandigarh", "Srinagar", "Jammu"
}

def generate_time_schedule():
    dep_h = random.randint(5, 23)
    dep_m = random.choice(["00", "15", "30", "45"])
    duration_h = random.randint(4, 14)
    duration_m = random.choice([0, 15, 30, 45])
    
    arr_mins_total = (dep_h * 60 + int(dep_m) + duration_h * 60 + duration_m) % (24 * 60)
    arr_h = arr_mins_total // 60
    arr_m = arr_mins_total % 60
    
    return f"{dep_h:02d}:{dep_m}", f"{arr_h:02d}:{arr_m:02d}", round(duration_h + duration_m/60.0, 1)

def seed_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    c = conn.cursor()

    print("Clearing existing data...")
    c.execute("DELETE FROM seats")
    c.execute("DELETE FROM bookings")
    c.execute("DELETE FROM buses")
    c.execute("DELETE FROM routes")
    c.execute("DELETE FROM districts")
    c.execute("DELETE FROM states")
    
    c.execute("DELETE FROM sqlite_sequence WHERE name IN ('seats', 'bookings', 'buses', 'routes', 'districts', 'states', 'users')")
    conn.commit()

    print("Seeding States & Union Territories...")
    state_id_map = {}
    for loc in INDIA_LOCATIONS:
        c.execute("INSERT INTO states (name, type) VALUES (?, ?)", (loc["state"], loc["type"]))
        state_id_map[loc["state"]] = c.lastrowid

    print("Seeding 787 Districts...")
    all_district_records = []
    
    for loc in INDIA_LOCATIONS:
        s_name = loc["state"]
        s_id = state_id_map[s_name]
        for d_name in loc["districts"]:
            is_maj = 1 if d_name in MAJOR_DISTRICT_NAMES or len(loc["districts"]) <= 3 else 0
            c.execute("INSERT INTO districts (state_id, name, is_major) VALUES (?, ?, ?)", (s_id, d_name, is_maj))
            all_district_records.append({"id": c.lastrowid, "state": s_name, "district": d_name, "is_major": is_maj})

    conn.commit()
    print(f"Seeded {len(all_district_records)} districts successfully!")

    print("Generating transport network routes & buses...")

    districts_by_state = {}
    for r in all_district_records:
        districts_by_state.setdefault(r["state"], []).append(r)

    routes_to_insert = []
    route_set = set()

    # 1. Intrastate routes: connect major districts to other districts in the same state
    for s_name, d_list in districts_by_state.items():
        majors = [d for d in d_list if d["is_major"] == 1]
        if not majors:
            majors = d_list[:2]
            
        for m in majors:
            for d in d_list:
                if m["id"] != d["id"]:
                    if (m["id"], d["id"]) not in route_set:
                        route_set.add((m["id"], d["id"]))
                        dist = random.randint(80, 450)
                        dur = round(dist / 45.0, 1)
                        routes_to_insert.append((m["id"], d["id"], dist, dur))
                    if (d["id"], m["id"]) not in route_set:
                        route_set.add((d["id"], m["id"]))
                        dist = random.randint(80, 450)
                        dur = round(dist / 45.0, 1)
                        routes_to_insert.append((d["id"], m["id"], dist, dur))

    # 2. Interstate routes between major hubs across states
    all_majors = [r for r in all_district_records if r["is_major"] == 1]
    for m1 in all_majors:
        other_majors = [m for m in all_majors if m["state"] != m1["state"]]
        selected_others = random.sample(other_majors, min(8, len(other_majors)))
        
        for m2 in selected_others:
            if (m1["id"], m2["id"]) not in route_set:
                route_set.add((m1["id"], m2["id"]))
                dist = random.randint(300, 1400)
                dur = round(dist / 55.0, 1)
                routes_to_insert.append((m1["id"], m2["id"], dist, dur))

    print(f"Creating {len(routes_to_insert)} transport routes...")
    
    global_bus_id = 1000
    for src_id, dest_id, dist, dur in routes_to_insert:
        c.execute(
            "INSERT INTO routes (source_district_id, destination_district_id, distance_km, estimated_duration_hrs) VALUES (?, ?, ?, ?)",
            (src_id, dest_id, dist, dur)
        )
        r_id = c.lastrowid

        # Generate 3-5 buses per route
        num_buses = random.randint(3, 5)
        for b_idx in range(num_buses):
            op = random.choice(OPERATORS)
            b_info = random.choice(BUS_TYPES)
            dep_t, arr_t, _ = generate_time_schedule()
            
            base_rate = 1.6 if "Volvo" in b_info["type"] or "Sleeper" in b_info["type"] else 1.1
            fare = float(round(dist * base_rate * b_info["base_multiplier"] + random.randint(-20, 50), -1))
            fare = max(250.0, fare)
            
            global_bus_id += 1
            op_code = "".join([w[0] for w in op.split()[:2]]).upper()
            bus_num = f"{op_code}-{r_id:04d}-{global_bus_id}"
            rating = round(random.uniform(4.2, 4.9), 1)

            c.execute('''
                INSERT INTO buses (bus_number, route_id, operator_name, bus_type, seat_layout, total_seats, departure_time, arrival_time, price, rating, amenities)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (bus_num, r_id, op, b_info["type"], b_info["layout"], b_info["seats"], dep_t, arr_t, fare, rating, b_info["amenities"]))

    conn.commit()

    # Get final counts
    c.execute("SELECT COUNT(*) FROM states")
    st_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM districts")
    dt_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM routes")
    rt_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM buses")
    bs_count = c.fetchone()[0]

    conn.close()

    print(f"Seeding completed successfully!")
    print(f"Summary: {st_count} States/UTs, {dt_count} Districts, {rt_count} Routes, {bs_count} Buses.")

if __name__ == '__main__':
    seed_db()
