"""
==============================================================================
Smart Bus Reservation System (ADS Transit Pro)
Developed & Architected by ADS Studio (Arandeep Singh Studio)
==============================================================================
"""

import base64
from datetime import datetime
import io
import os
import sqlite3
import uuid
from flask import Flask, flash, redirect, render_template, request, url_for
import qrcode
from init_db import ensure_db_exists

# Initialize Database on Application Startup
ensure_db_exists()

# Initialize Flask Application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

def get_db_connection():
    """Establish and return a SQLite database connection with row factory."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Master list of Indian States & Union Territories for route selection
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

@app.route('/')
def index():
    """Render application homepage with departure and destination state selectors."""
    return render_template('index.html', sources=INDIAN_STATES, destinations=INDIAN_STATES)

@app.route('/buses', methods=['GET', 'POST'])
def buses():
    """Query available buses based on departure city, destination, date, and bus type."""
    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        date = request.form.get('date')
        bus_type = request.form.get('bus_type', '')

        conn = get_db_connection()
        
        query = '''
            SELECT b.*, r.source, r.destination 
            FROM buses b 
            JOIN routes r ON b.route_id = r.id 
            WHERE r.source = ? AND r.destination = ?
        '''
        params = [source, destination]
        
        if bus_type and bus_type != 'All':
            query += ' AND b.bus_type = ?'
            params.append(bus_type)
            
        available_buses = conn.execute(query, tuple(params)).fetchall()
        conn.close()
        return render_template('buses.html', buses=available_buses, source=source, destination=destination, date=date)
    
    return redirect(url_for('index'))

@app.route('/book/<int:bus_id>', methods=['GET', 'POST'])
def book(bus_id):
    """Handle seat selection, passenger details submission, and booking confirmation."""
    date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    conn = get_db_connection()
    bus = conn.execute(
        'SELECT b.*, r.source, r.destination FROM buses b JOIN routes r ON b.route_id = r.id WHERE b.id = ?', 
        (bus_id,)
    ).fetchone()
    
    if not bus:
        conn.close()
        flash('Selected bus route not found.')
        return redirect(url_for('index'))
        
    # Fetch list of already booked seat numbers for this bus & date
    booked_seats_records = conn.execute(
        'SELECT seat_number FROM seats WHERE bus_id = ? AND date = ? AND is_booked = 1', 
        (bus_id, date)
    ).fetchall()
    booked_seats = [record['seat_number'] for record in booked_seats_records]
    conn.close()
    
    if request.method == 'POST':
        selected_seats = request.form.get('selected_seats')  # comma separated seat numbers
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')
        
        if not selected_seats:
            flash('Please select at least one seat before confirming.')
            return redirect(url_for('book', bus_id=bus_id, date=date))
            
        seats_list = [s.strip() for s in selected_seats.split(',') if s.strip()]
        total_price = len(seats_list) * bus['price']
        booking_ref = str(uuid.uuid4())[:8].upper()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Register user profile
            cursor.execute(
                'INSERT INTO users (name, age, gender, phone, email) VALUES (?, ?, ?, ?, ?)', 
                (name, age, gender, phone, email)
            )
            user_id = cursor.lastrowid
            
            # Record booking entry
            cursor.execute(
                'INSERT INTO bookings (booking_ref, user_id, bus_id, date, seat_numbers, total_price, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                (booking_ref, user_id, bus_id, date, ",".join(seats_list), total_price, 'PAID')
            )
            
            # Reserve individual seats
            for seat in seats_list:
                existing = cursor.execute(
                    'SELECT * FROM seats WHERE bus_id = ? AND date = ? AND seat_number = ? AND is_booked = 1', 
                    (bus_id, date, seat)
                ).fetchone()
                
                if existing:
                    conn.rollback()
                    flash(f'Seat {seat} has already been reserved by another passenger!')
                    return redirect(url_for('book', bus_id=bus_id, date=date))
                
                cursor.execute(
                    'INSERT INTO seats (bus_id, date, seat_number, is_booked) VALUES (?, ?, ?, 1)', 
                    (bus_id, date, seat)
                )
                
            conn.commit()
        except Exception as e:
            conn.rollback()
            flash('An error occurred while processing your reservation.')
            print(f"Booking Error Trace: {e}")
            return redirect(url_for('book', bus_id=bus_id, date=date))
        finally:
            conn.close()
        
        # Log simulated confirmation dispatch
        print(f"\n--- ADS TRANSIT PRO DISPATCH ---")
        print(f"To: {email}")
        print(f"Subject: e-Ticket Confirmation - {booking_ref}")
        print(f"Passenger: {name}\nRoute: {bus['source']} -> {bus['destination']}\nSeats: {','.join(seats_list)}\nAmount: INR {total_price}")
        print(f"---------------------------------\n")
        
        return redirect(url_for('ticket', booking_ref=booking_ref))
        
    return render_template('booking.html', bus=bus, date=date, booked_seats=booked_seats)

@app.route('/ticket/<booking_ref>')
def ticket(booking_ref):
    """Render confirmed e-Ticket pass with base64 encoded QR verification code."""
    conn = get_db_connection()
    booking = conn.execute('''
        SELECT b.*, u.name, u.email, u.phone, bus.bus_number, bus.departure_time, bus.arrival_time, r.source, r.destination 
        FROM bookings b 
        JOIN users u ON b.user_id = u.id 
        JOIN buses bus ON b.bus_id = bus.id 
        JOIN routes r ON bus.route_id = r.id
        WHERE b.booking_ref = ?
    ''', (booking_ref,)).fetchone()
    conn.close()
    
    if not booking:
        return "Booking record not found", 404
        
    # Generate dynamic verification QR code payload
    qr_payload = f"Booking Ref: {booking['booking_ref']} | Passenger: {booking['name']} | Bus: {booking['bus_number']} | Date: {booking['date']} | Seats: {booking['seat_numbers']}"
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(qr_payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    qr_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    return render_template('ticket.html', booking=booking, qr_base64=qr_base64)

@app.route('/admin', methods=['GET'])
def admin():
    """Render administration dashboard with routes, buses, and booking analytics."""
    conn = get_db_connection()
    routes = conn.execute('SELECT * FROM routes').fetchall()
    buses = conn.execute('SELECT b.*, r.source, r.destination FROM buses b JOIN routes r ON b.route_id = r.id').fetchall()
    bookings = conn.execute('''
        SELECT b.id, b.booking_ref, b.date, b.seat_numbers, b.total_price, b.payment_status, 
               u.name, bus.bus_number, r.source, r.destination
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN buses bus ON b.bus_id = bus.id
        JOIN routes r ON bus.route_id = r.id
        ORDER BY b.id DESC
    ''').fetchall()
    conn.close()
    return render_template('admin.html', routes=routes, buses=buses, bookings=bookings, indian_states=INDIAN_STATES)

@app.route('/admin/add_route', methods=['POST'])
def add_route():
    """Create a new route in the database."""
    source = request.form['source']
    destination = request.form['destination']
    conn = get_db_connection()
    conn.execute('INSERT INTO routes (source, destination) VALUES (?, ?)', (source, destination))
    conn.commit()
    conn.close()
    flash('New route added successfully!')
    return redirect(url_for('admin'))

@app.route('/admin/add_bus', methods=['POST'])
def add_bus():
    """Configure a new bus service for an existing route."""
    bus_number = request.form['bus_number']
    route_id = request.form['route_id']
    bus_type = request.form['bus_type']
    total_seats = request.form['total_seats']
    departure_time = request.form['departure_time']
    arrival_time = request.form['arrival_time']
    price = request.form['price']
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO buses (bus_number, route_id, bus_type, total_seats, departure_time, arrival_time, price) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (bus_number, route_id, bus_type, total_seats, departure_time, arrival_time, price)
    )
    conn.commit()
    conn.close()
    flash('New bus service configured successfully!')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
