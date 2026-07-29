<div align="center">

  <br>

  <!-- ADS Studio Logo Image Banner -->
  <a href="https://github.com/Arandeep12/smart-bus-reservation-system">
    <img src="static/ads_logo.jpg" alt="ADS Studio — ADS Transit Pro" width="240" style="border-radius: 16px; box-shadow: 0 12px 36px rgba(0,0,0,0.35); border: 1px solid rgba(212,175,55,0.4);">
  </a>

  <br><br>

  <!-- Product Title & Subtitle -->
  <h1>ADS Transit Pro</h1>
  <h3>Smart Bus Reservation System</h3>

  <p>
    <em>Enterprise-Grade Intercity Bus Booking & Reservation SaaS Platform</em>
  </p>

  <p>
    Designed & Developed by <strong><a href="https://github.com/Arandeep12">ADS Studio</a></strong> (Arandeep Singh Studio)
  </p>

  <br>

  <!-- Badges -->
  <p>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"></a>
    <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask Version"></a>
    <a href="https://www.sqlite.org/"><img src="https://img.shields.io/badge/Database-SQLite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite3"></a>
    <a href="https://developer.mozilla.org/"><img src="https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20ES6%2B-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="Frontend Stack"></a>
    <a href="#-responsive-screen-compatibility"><img src="https://img.shields.io/badge/Responsive-320px%20to%204K-22C55E?style=for-the-badge&logo=responsive&logoColor=white" alt="Responsive"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License"></a>
  </p>

  <br>

</div>

---

## 📌 Executive Summary

**ADS Transit Pro** (Smart Bus Reservation System) is an enterprise-grade, full-stack intercity bus reservation platform built to deliver an airline-quality seat booking experience. Designed from the ground up by **ADS Studio**, the application features real-time interactive seat layouts, instant QR code e-ticket generation, dynamic fare calculation, multi-device mobile-first responsive interfaces, and a feature-rich admin dashboard.

Engineered with **Python Flask**, **SQLite3**, and a custom **CSS Glassmorphism Design System**, ADS Transit Pro combines high-concurrency seat reservation logic with an intuitive human-centered user interface.

---

## ✨ Key Features

### 🚌 Passenger Booking Experience
- **Interactive Search Engine**: Search intercity buses across all 28 Indian States & 8 Union Territories with journey date limits and bus type filters (AC, Non-AC, Sleeper).
- **Airline-Style Seat Selection**: Visual 2D interactive bus interior map displaying driver cabin, entry door, aisle, and real-time seat status (Available, Booked, Selected).
- **Live Fare Breakdown Engine**: Real-time summary calculation factoring base fare, 5% GST, and convenience fees.
- **Instant QR e-Ticket Generation**: Dynamic Base64-encoded QR verification code generated upon payment confirmation.
- **PDF Export & Print**: One-click browser print and vector PDF ticket export using `html2pdf.js`.

### 🛡️ Enterprise & Admin Portal
- **Dashboard Analytics**: Real-time revenue reporting, active booking counters, bus fleet status, and route metrics.
- **Route & Fleet Manager**: Dynamic route creator and bus schedule dispatcher supporting custom seat capacities, pricing, and timetable pairs.
- **Booking Ledger**: Searchable booking log showing passenger records, assigned seats, payment statuses, and reference codes.

### 🎨 Mobile-First UI/UX & Architecture
- **ADS Studio Branding**: Official gold-embossed brand identity integrated across navbar, splash screen, footer, and dedicated About section.
- **Fluid Clamp Typography**: Responsive CSS `clamp()` typography eliminating zoom issues on any viewport.
- **Touch-Friendly Controls**: Minimum 44px tap targets for mobile usability across 320px (Small Android) to 4K displays.
- **Mobile Table Transformations**: Data tables automatically convert to responsive stacked cards on small screens (`data-label`).
- **Toast Notifications**: Built-in alert system for seat selection, route swaps, and validation feedback.

---

## 🛠️ Technology Stack

| Component | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Backend Core** | Python 3.10+ / Flask 3.0 | Application server, routing, session handling |
| **WSGI Server** | Gunicorn 21.2+ | Production-grade HTTP WSGI server for Cloud / Render |
| **Database** | SQLite3 | Relational data store for routes, buses, seats, & bookings |
| **QR Code Engine** | `qrcode` + `Pillow` (PIL) | Dynamic matrix QR code rendering for tickets |
| **Frontend Styling** | Custom CSS3 Custom Properties | Glassmorphism design system, grid, flexbox, clamp() typography |
| **Icons Library** | Lucide Icons (SVG) | Lightweight vector icon suite |
| **PDF Generation** | `html2pdf.js` / `html2canvas` | Client-side e-ticket PDF generation |

---

## 📁 Repository Structure

```text
smart-bus-reservation-system/
├── app.py                  # Main Flask application & WSGI entry point
├── init_db.py              # Database schema initializer (Auto-run on startup)
├── seed_db.py              # Mock data generator (Routes, Buses, Seats)
├── Procfile                # Heroku / Render deployment process file
├── render.yaml             # Render Blueprint Infrastructure-as-Code
├── requirements.txt        # Python package dependencies (Flask, Gunicorn, etc.)
├── LICENSE                 # Open-source MIT License
├── README.md               # Repository documentation
├── .gitignore              # Ignored files & runtime environment rules
├── static/                 # Static web assets
│   ├── ads_logo.jpg        # Official ADS Studio branding logo
│   ├── ads_logo_square.jpg # Square icon logo variant
│   ├── favicon.ico         # 32x32 browser tab icon
│   ├── favicon.png         # 180x180 mobile touch icon
│   └── style.css           # ADS Transit Pro Design System stylesheet
└── templates/              # Jinja2 HTML5 Templates
    ├── base.html           # Master layout template (Navbar, Footer, Toasts)
    ├── index.html          # Homepage, search widget, features & About section
    ├── buses.html          # Bus listing page with live search & sort
    ├── booking.html        # Airline seat selection map & passenger form
    ├── ticket.html         # Confirmed e-Ticket pass with QR code
    └── admin.html          # Admin dashboard & route/bus management
```

---

## ⚡ Quickstart & Installation

Follow these steps to set up and run **ADS Transit Pro** locally on your machine.

### Prerequisites
- **Python 3.10** or higher installed
- **pip** package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/Arandeep12/smart-bus-reservation-system.git
cd smart-bus-reservation-system
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize & Seed Database
```bash
# Create database schema and default sample routes
python init_db.py

# (Optional) Generate comprehensive routes across 1,260 state combinations
python seed_db.py
```

### Step 5: Launch Application
```bash
python app.py
```

Open your browser and navigate to **`http://127.0.0.1:5000`**.

---

## 🌐 Deploying to Render

**ADS Transit Pro** is fully pre-configured for instant zero-downtime deployment on **[Render](https://render.com)**.

### Option A: Automatic Blueprint Deployment (Recommended)
1. Fork or push this repository to your GitHub account (`Arandeep12/smart-bus-reservation-system`).
2. Log in to [Render Dashboard](https://dashboard.render.com/) and click **New +** → **Blueprint**.
3. Connect your GitHub repository.
4. Render will automatically detect `render.yaml` and configure the Web Service with:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **Apply**. Render will build and deploy the web service automatically.

### Option B: Manual Web Service Setup on Render
If configuring manually without `render.yaml`:
- **Service Type**: Web Service
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Auto Database Setup**: The application automatically checks and initializes `database.db` with default routes and sample buses on first launch.

---

## 🚀 Usage Guide

### Passenger Flow
1. **Search Route**: Select departure state, destination state, date of travel, and preferred bus type on the homepage.
2. **Filter & Select Bus**: Browse available bus services, filter by AC/Sleeper, sort by fare or schedule, and click **Select Seats**.
3. **Choose Seats**: Click available seats on the 2D interactive bus map to review real-time pricing and fare breakdown.
4. **Enter Passenger Info**: Complete full name, age, gender, phone number, and simulated payment credentials.
5. **Receive e-Ticket**: View confirmed e-ticket with scannable QR verification code. Print or download as PDF.

### Administrator Flow
1. Navigate to **`http://127.0.0.1:5000/admin`**.
2. **Analytics Overview**: View total bookings, accumulated revenue, active bus fleet count, and registered routes.
3. **Manage Routes**: Add new interstate route pairs.
4. **Manage Buses**: Dispatch new bus numbers with custom departure times, seat counts, and pricing per seat.

---

## 📱 Responsive Screen Compatibility

Tested across all major mobile, tablet, and desktop display resolutions:
- 📱 **Small Mobile (320px – 430px)**: iPhone SE, iPhone 14/15 Pro Max, Samsung Galaxy series.
- 📱 **Tablets (768px – 1024px)**: iPad Mini, iPad Air, iPad Pro.
- 💻 **Laptops & Desktops (1280px – 4K)**: MacBook Air/Pro, Windows Laptops, 1440p & 4K Monitors.

---

## 🔮 Future Enhancements Roadmap

- [ ] **Live GPS Tracking**: Integrate Real-time bus location tracking via WebSockets.
- [ ] **SMS & WhatsApp Dispatch**: Automated e-ticket notifications via Twilio / WhatsApp API.
- [ ] **Payment Gateway Integration**: Razorpay / Stripe live payment gateway checkout.
- [ ] **Multi-Language Support**: i18n support for Hindi, Tamil, Telugu, and English.

---

## 🤝 Contribution Guidelines

Contributions are welcome! If you would like to report a bug or suggest a feature:
1. Fork the project repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 👨‍💻 Author & Credits

Designed & Developed with ❤️ by **[ADS Studio](https://github.com/Arandeep12)** (Arandeep Singh Studio).

- **Project Lead**: Arandeep Singh
- **Organization**: ADS Studio
- **Copyright**: © 2026 ADS Studio. All Rights Reserved.
