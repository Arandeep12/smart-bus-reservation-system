"""
==============================================================================
Smart Bus Reservation System (ADS Transit Pro) — Production SaaS Backend
Developed & Architected by ADS Studio (Arandeep Singh Studio)
==============================================================================
"""

import base64
from datetime import datetime
import io
import os
import random
import sqlite3
import uuid
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
import qrcode

from init_db import DB_PATH, ensure_db_exists

# Initialize Database Schema & Seed Data on Startup
ensure_db_exists()

# Initialize Flask Application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey_ads_transit_pro_2026')

def get_db_connection():
    """Establish and return a SQLite database connection with row factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

# Helper operators and bus specs for dynamic on-demand route provisioning
OPERATORS = [
    "ADS Express", "KSRTC Swift", "MSRTC Shivneri", "UPSRTC Janrath",
    "Zingbus Premium", "IntrCity SmartBus", "VRL Travels", "SRS Travels",
    "Orange Tours & Travels", "Hans Travels", "Mahalaxmi Travels", "Raj National Express"
]

BUS_SPECS = [
    {"type": "Volvo Multi-Axle AC (2+2)", "layout": "2x2", "seats": 40, "mult": 1.5, "amenities": "WiFi, Charging, Water, Blanket, Live Tracking"},
    {"type": "AC Sleeper (2+1)", "layout": "2x1", "seats": 30, "mult": 1.8, "amenities": "Personal TV, Charging, Pillow, Blanket, Reading Light"},
    {"type": "Luxury Semi-Sleeper AC (2+2)", "layout": "2x2", "seats": 44, "mult": 1.3, "amenities": "WiFi, Charging, Water Bottle, Reclining Seats"},
    {"type": "Non-AC Seater (2+2)", "layout": "2x2", "seats": 48, "mult": 0.9, "amenities": "Charging Port, Emergency Button"}
]

def auto_provision_route(conn, src_district_id, dest_district_id):
    """
    Guarantees search never fails!
    If no route exists in DB between two valid districts, dynamically provisions a new route and buses.
    """
    cursor = conn.cursor()

    # Check if route already exists
    route = cursor.execute(
        "SELECT * FROM routes WHERE source_district_id = ? AND destination_district_id = ?",
        (src_district_id, dest_district_id)
    ).fetchone()

    if not route:
        dist = random.randint(120, 600)
        dur = round(dist / 48.0, 1)
        cursor.execute(
            "INSERT INTO routes (source_district_id, destination_district_id, distance_km, estimated_duration_hrs) VALUES (?, ?, ?, ?)",
            (src_district_id, dest_district_id, dist, dur)
        )
        route_id = cursor.lastrowid
        route = cursor.execute("SELECT * FROM routes WHERE id = ?", (route_id,)).fetchone()
    else:
        route_id = route['id']

    # Check if buses exist on this route
    existing_buses = cursor.execute("SELECT COUNT(*) FROM buses WHERE route_id = ?", (route_id,)).fetchone()[0]
    
    if existing_buses == 0:
        dist = route['distance_km'] or 300
        for i in range(4):
            op = random.choice(OPERATORS)
            spec = random.choice(BUS_SPECS)
            dep_h = (6 + i * 4) % 24
            dep_m = random.choice(["00", "30"])
            arr_h = (dep_h + int(dist / 50)) % 24
            dep_t = f"{dep_h:02d}:{dep_m}"
            arr_t = f"{arr_h:02d}:{dep_m}"

            fare = float(round(dist * 1.4 * spec["mult"] + random.randint(10, 40), -1))
            fare = max(300.0, fare)
            
            global_id = random.randint(10000, 99999)
            op_code = "".join([w[0] for w in op.split()[:2]]).upper()
            bus_num = f"{op_code}-{route_id:04d}-{global_id}"
            rating = round(random.uniform(4.3, 4.9), 1)

            cursor.execute('''
                INSERT INTO buses (bus_number, route_id, operator_name, bus_type, seat_layout, total_seats, departure_time, arrival_time, price, rating, amenities)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (bus_num, route_id, op, spec["type"], spec["layout"], spec["seats"], dep_t, arr_t, fare, rating, spec["amenities"]))
            
        conn.commit()

    return route_id

# ----------------------------------------------------------------------------
# API ENDPOINTS
# ----------------------------------------------------------------------------

@app.route('/api/districts', methods=['GET'])
def get_districts():
    """API endpoint to fetch districts by state ID or state name for cascading dropdowns."""
    state_id = request.args.get('state_id')
    state_name = request.args.get('state_name')

    conn = get_db_connection()
    if state_id:
        districts = conn.execute(
            "SELECT id, name FROM districts WHERE state_id = ? ORDER BY name ASC", 
            (state_id,)
        ).fetchall()
    elif state_name:
        districts = conn.execute(
            "SELECT d.id, d.name FROM districts d JOIN states s ON d.state_id = s.id WHERE s.name = ? ORDER BY d.name ASC", 
            (state_name,)
        ).fetchall()
    else:
        districts = conn.execute("SELECT id, name, state_id FROM districts ORDER BY name ASC").fetchall()
    
    conn.close()
    return jsonify([dict(row) for row in districts])

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """API endpoint returning full hierarchy of States/UTs and their Districts."""
    conn = get_db_connection()
    states = conn.execute("SELECT * FROM states ORDER BY name ASC").fetchall()
    result = []
    for s in states:
        districts = conn.execute(
            "SELECT id, name, is_major FROM districts WHERE state_id = ? ORDER BY name ASC", 
            (s['id'],)
        ).fetchall()
        result.append({
            "id": s['id'],
            "name": s['name'],
            "type": s['type'],
            "districts": [dict(d) for d in districts]
        })
    conn.close()
    return jsonify(result)

# ----------------------------------------------------------------------------
# APPLICATION ROUTES
# ----------------------------------------------------------------------------

@app.route('/')
def index():
    """Render application homepage with cascading State/UT & District selectors."""
    conn = get_db_connection()
    states = conn.execute("SELECT * FROM states ORDER BY name ASC").fetchall()
    
    # Default initial districts for popular states (e.g. Punjab, Maharashtra, Delhi, Tamil Nadu)
    default_districts = conn.execute(
        "SELECT d.id, d.name, s.name as state_name FROM districts d JOIN states s ON d.state_id = s.id ORDER BY d.name ASC"
    ).fetchall()
    
    conn.close()
    return render_template('index.html', states=states, default_districts=default_districts)

@app.route('/buses', methods=['GET', 'POST'])
def buses():
    """Query available buses based on departure district, destination district, date, and bus type."""
    if request.method == 'POST':
        source_district_id = request.form.get('source_district')
        destination_district_id = request.form.get('destination_district')
        source_state_id = request.form.get('source_state')
        destination_state_id = request.form.get('destination_state')
        date = request.form.get('date', datetime.today().strftime('%Y-%m-%d'))
        bus_type = request.form.get('bus_type', 'All')
        passengers = int(request.form.get('passengers', 1))
    else:
        source_district_id = request.args.get('source_district')
        destination_district_id = request.args.get('destination_district')
        source_state_id = request.args.get('source_state')
        destination_state_id = request.args.get('destination_state')
        date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
        bus_type = request.args.get('bus_type', 'All')
        passengers = int(request.args.get('passengers', 1))

    conn = get_db_connection()

    # Resolve source and destination details
    src_district = None
    dest_district = None

    if source_district_id:
        src_district = conn.execute(
            "SELECT d.*, s.name as state_name FROM districts d JOIN states s ON d.state_id = s.id WHERE d.id = ?",
            (source_district_id,)
        ).fetchone()

    if destination_district_id:
        dest_district = conn.execute(
            "SELECT d.*, s.name as state_name FROM districts d JOIN states s ON d.state_id = s.id WHERE d.id = ?",
            (destination_district_id,)
        ).fetchone()

    # Fallback to defaults if missing
    if not src_district or not dest_district:
        all_districts = conn.execute("SELECT id FROM districts LIMIT 2").fetchall()
        if not src_district:
            src_district = conn.execute("SELECT d.*, s.name as state_name FROM districts d JOIN states s ON d.state_id = s.id WHERE d.id = ?", (all_districts[0]['id'],)).fetchone()
        if not dest_district:
            dest_district = conn.execute("SELECT d.*, s.name as state_name FROM districts d JOIN states s ON d.state_id = s.id WHERE d.id = ?", (all_districts[1]['id'],)).fetchone()

    src_id = src_district['id']
    dest_id = dest_district['id']

    # Auto-provision route and buses if none exist for this specific pair
    auto_provision_route(conn, src_id, dest_id)

    # Fetch matching buses
    query = '''
        SELECT b.*, r.distance_km, r.estimated_duration_hrs,
               sd.name as source_district, ss.name as source_state,
               dd.name as destination_district, ds.name as destination_state
        FROM buses b
        JOIN routes r ON b.route_id = r.id
        JOIN districts sd ON r.source_district_id = sd.id
        JOIN states ss ON sd.state_id = ss.id
        JOIN districts dd ON r.destination_district_id = dd.id
        JOIN states ds ON dd.state_id = ds.id
        WHERE r.source_district_id = ? AND r.destination_district_id = ?
    '''
    params = [src_id, dest_id]

    if bus_type and bus_type != 'All':
        query += ' AND b.bus_type LIKE ?'
        params.append(f'%{bus_type}%')

    query += ' ORDER BY b.price ASC'

    available_buses_raw = conn.execute(query, tuple(params)).fetchall()

    # Process live available seats count per bus for requested date
    buses_list = []
    for b in available_buses_raw:
        bus_dict = dict(b)
        booked_count = conn.execute(
            "SELECT COUNT(*) FROM seats WHERE bus_id = ? AND date = ? AND is_booked = 1",
            (bus_dict['id'], date)
        ).fetchone()[0]
        bus_dict['available_seats'] = bus_dict['total_seats'] - booked_count
        buses_list.append(bus_dict)

    conn.close()

    return render_template(
        'buses.html',
        buses=buses_list,
        source_district=src_district['name'],
        source_state=src_district['state_name'],
        destination_district=dest_district['name'],
        destination_state=dest_district['state_name'],
        date=date,
        passengers=passengers,
        bus_type=bus_type
    )

@app.route('/book/<int:bus_id>', methods=['GET', 'POST'])
def book(bus_id):
    """Handle seat selection, passenger details, and instant reservation."""
    date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    conn = get_db_connection()

    bus = conn.execute('''
        SELECT b.*, r.distance_km, r.estimated_duration_hrs,
               sd.name as source, ss.name as source_state,
               dd.name as destination, ds.name as destination_state
        FROM buses b
        JOIN routes r ON b.route_id = r.id
        JOIN districts sd ON r.source_district_id = sd.id
        JOIN states ss ON sd.state_id = ss.id
        JOIN districts dd ON r.destination_district_id = dd.id
        JOIN states ds ON dd.state_id = ds.id
        WHERE b.id = ?
    ''', (bus_id,)).fetchone()

    if not bus:
        conn.close()
        flash('Selected bus service not found.')
        return redirect(url_for('index'))

    # Fetch list of already booked seat numbers for this bus & date
    booked_records = conn.execute(
        'SELECT seat_number FROM seats WHERE bus_id = ? AND date = ? AND is_booked = 1',
        (bus_id, date)
    ).fetchall()
    booked_seats = [r['seat_number'] for r in booked_records]
    conn.close()

    if request.method == 'POST':
        selected_seats = request.form.get('selected_seats')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if not selected_seats:
            flash('Please select at least one seat before confirming your booking.')
            return redirect(url_for('book', bus_id=bus_id, date=date))

        seats_list = [s.strip() for s in selected_seats.split(',') if s.strip()]
        passengers_count = len(seats_list)
        base_fare = passengers_count * bus['price']
        gst = base_fare * 0.05
        conv_fee = 29.0
        total_price = base_fare + gst + conv_fee

        booking_ref = f"ADS-{str(uuid.uuid4())[:8].upper()}"

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Register user
            cursor.execute(
                'INSERT INTO users (name, age, gender, phone, email) VALUES (?, ?, ?, ?, ?)',
                (name, age, gender, phone, email)
            )
            user_id = cursor.lastrowid

            # Create booking entry
            cursor.execute('''
                INSERT INTO bookings (booking_ref, user_id, bus_id, date, seat_numbers, passengers_count, total_price, payment_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (booking_ref, user_id, bus_id, date, ",".join(seats_list), passengers_count, total_price, 'PAID'))

            # Reserve individual seats atomically
            for seat in seats_list:
                existing = cursor.execute(
                    'SELECT * FROM seats WHERE bus_id = ? AND date = ? AND seat_number = ? AND is_booked = 1',
                    (bus_id, date, seat)
                ).fetchone()

                if existing:
                    conn.rollback()
                    flash(f'Seat {seat} was just reserved by another passenger. Please select another seat.')
                    return redirect(url_for('book', bus_id=bus_id, date=date))

                cursor.execute(
                    'INSERT OR REPLACE INTO seats (bus_id, date, seat_number, is_booked) VALUES (?, ?, ?, 1)',
                    (bus_id, date, seat)
                )

            conn.commit()
        except Exception as e:
            conn.rollback()
            flash('An unexpected error occurred while processing your reservation. Please try again.')
            print(f"Booking Error Trace: {e}")
            return redirect(url_for('book', bus_id=bus_id, date=date))
        finally:
            conn.close()

        return redirect(url_for('ticket', booking_ref=booking_ref))

    return render_template('booking.html', bus=bus, date=date, booked_seats=booked_seats)

@app.route('/ticket/<booking_ref>')
def ticket(booking_ref):
    """Render confirmed e-Ticket pass with base64 encoded QR verification code."""
    conn = get_db_connection()
    booking = conn.execute('''
        SELECT b.*, u.name, u.email, u.phone, u.age, u.gender,
               bus.bus_number, bus.operator_name, bus.bus_type, bus.departure_time, bus.arrival_time,
               sd.name as source, ss.name as source_state,
               dd.name as destination, ds.name as destination_state
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN buses bus ON b.bus_id = bus.id
        JOIN routes r ON bus.route_id = r.id
        JOIN districts sd ON r.source_district_id = sd.id
        JOIN states ss ON sd.state_id = ss.id
        JOIN districts dd ON r.destination_district_id = dd.id
        JOIN states ds ON dd.state_id = ds.id
        WHERE b.booking_ref = ?
    ''', (booking_ref,)).fetchone()
    conn.close()

    if not booking:
        return "e-Ticket record not found", 404

    # Generate QR verification payload
    qr_payload = f"ADS TRANSIT PRO e-TICKET\nRef: {booking['booking_ref']}\nPassenger: {booking['name']}\nRoute: {booking['source']} ({booking['source_state']}) -> {booking['destination']} ({booking['destination_state']})\nBus: {booking['bus_number']} ({booking['operator_name']})\nDate: {booking['date']}\nSeats: {booking['seat_numbers']}\nStatus: VERIFIED PAID"
    
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(qr_payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1E1B4B", back_color="white")

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    qr_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return render_template('ticket.html', booking=booking, qr_base64=qr_base64)

@app.route('/admin', methods=['GET'])
def admin():
    """Render comprehensive administration dashboard."""
    conn = get_db_connection()

    states = conn.execute("SELECT * FROM states ORDER BY name ASC").fetchall()
    districts = conn.execute(
        "SELECT d.*, s.name as state_name FROM districts d JOIN states s ON d.state_id = s.id ORDER BY s.name, d.name ASC"
    ).fetchall()

    routes = conn.execute('''
        SELECT r.*, sd.name as source_district, ss.name as source_state,
               dd.name as destination_district, ds.name as destination_state
        FROM routes r
        JOIN districts sd ON r.source_district_id = sd.id
        JOIN states ss ON sd.state_id = ss.id
        JOIN districts dd ON r.destination_district_id = dd.id
        JOIN states ds ON dd.state_id = ds.id
        ORDER BY r.id DESC LIMIT 100
    ''').fetchall()

    buses = conn.execute('''
        SELECT b.*, sd.name as source_district, dd.name as destination_district
        FROM buses b
        JOIN routes r ON b.route_id = r.id
        JOIN districts sd ON r.source_district_id = sd.id
        JOIN districts dd ON r.destination_district_id = dd.id
        ORDER BY b.id DESC LIMIT 100
    ''').fetchall()

    bookings = conn.execute('''
        SELECT b.*, u.name, u.email, bus.bus_number, bus.operator_name,
               sd.name as source_district, dd.name as destination_district
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN buses bus ON b.bus_id = bus.id
        JOIN routes r ON bus.route_id = r.id
        JOIN districts sd ON r.source_district_id = sd.id
        JOIN districts dd ON r.destination_district_id = dd.id
        ORDER BY b.id DESC
    ''').fetchall()

    conn.close()

    return render_template(
        'admin.html',
        states=states,
        districts=districts,
        routes=routes,
        buses=buses,
        bookings=bookings
    )

@app.route('/admin/add_route', methods=['POST'])
def add_route():
    """Add a new district-to-district route."""
    src_dist_id = request.form['source_district_id']
    dest_dist_id = request.form['destination_district_id']
    dist_km = request.form.get('distance_km', 350)
    dur_hrs = request.form.get('estimated_duration_hrs', 7.5)

    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO routes (source_district_id, destination_district_id, distance_km, estimated_duration_hrs) VALUES (?, ?, ?, ?)',
            (src_dist_id, dest_dist_id, dist_km, dur_hrs)
        )
        conn.commit()
        flash('New district route created successfully!')
    except sqlite3.IntegrityError:
        flash('Route between selected districts already exists.')
    finally:
        conn.close()

    return redirect(url_for('admin'))

@app.route('/admin/add_bus', methods=['POST'])
def add_bus():
    """Add a new bus service for an existing route."""
    bus_number = request.form['bus_number']
    route_id = request.form['route_id']
    operator_name = request.form.get('operator_name', 'ADS Express')
    bus_type = request.form['bus_type']
    seat_layout = request.form.get('seat_layout', '2x2')
    total_seats = int(request.form.get('total_seats', 40))
    departure_time = request.form['departure_time']
    arrival_time = request.form['arrival_time']
    price = float(request.form['price'])
    amenities = request.form.get('amenities', 'WiFi, Charging, Reclining Seats')

    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO buses (bus_number, route_id, operator_name, bus_type, seat_layout, total_seats, departure_time, arrival_time, price, rating, amenities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 4.5, ?)
        ''', (bus_number, route_id, operator_name, bus_type, seat_layout, total_seats, departure_time, arrival_time, price, amenities))
        conn.commit()
        flash('New bus service added successfully!')
    except sqlite3.IntegrityError:
        flash('Bus number already registered. Please use a unique bus number.')
    finally:
        conn.close()

    return redirect(url_for('admin'))

@app.route('/admin/seed_db', methods=['POST'])
def trigger_seed():
    """Trigger full database re-seeding from admin dashboard."""
    from seed_db import seed_db
    seed_db()
    flash('Database re-seeded successfully with 787 districts and full bus network!')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except OSError as e:
        if 'Address already in use' in str(e) or getattr(e, 'errno', None) == 48:
            print("\n[ADS Transit Pro] Port 5000 is reserved by macOS AirPlay Receiver. Launching on http://127.0.0.1:5050/\n")
            app.run(host='0.0.0.0', port=5050, debug=False)
        else:
            raise e

