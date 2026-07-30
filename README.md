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
    <a href="https://www.reportlab.com/"><img src="https://img.shields.io/badge/PDF_Engine-ReportLab%20%2F%20xhtml2pdf-E11D48?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="PDF Engine"></a>
    <a href="https://developer.mozilla.org/"><img src="https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20ES6%2B-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="Frontend Stack"></a>
    <a href="#-responsive-screen-compatibility"><img src="https://img.shields.io/badge/Responsive-320px%20to%204K-22C55E?style=for-the-badge&logo=responsive&logoColor=white" alt="Responsive"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License"></a>
  </p>

  <br>

</div>

---

## 📌 Executive Summary

**ADS Transit Pro** (Smart Bus Reservation System) is an enterprise-grade, full-stack intercity bus reservation platform built to deliver an airline-quality seat booking experience. Architected from the ground up by **ADS Studio**, the platform features real-time interactive seat selection maps, instant matrix QR code e-ticket generation, server-side commercial vector PDF export, dynamic fare calculation across India's 28 States & 787 Districts, multi-device mobile-first responsive interfaces, and a feature-rich SaaS administrative portal.

Engineered with **Python Flask**, **SQLite3**, **ReportLab / xhtml2pdf**, and a custom **CSS Glassmorphism Design System**, ADS Transit Pro combines high-concurrency seat reservation logic with an intuitive human-centered user interface.

---

## 🌐 Live Demo

**🚀 [https://ads-transit-pro.onrender.com](https://ads-transit-pro.onrender.com)**

---

## 📸 Application Screenshots

Explore the complete end-to-end passenger booking flow and administration suite of **ADS Transit Pro**.

### 🏠 Home Page & Hero Section
![Home Page](screenshots/home.png)

### ℹ️ About ADS Transit Pro & Platform Vision
![About Section](screenshots/About.png)

### 🔍 Smart Intercity Bus Search Engine
![Search Bus](screenshots/search.png)

### 🚌 Search Results & Live Bus Listings
![Search Results](screenshots/search_result.png)

### 🔀 Search Results — Alternate Fleet View
![Search Results Alternative](screenshots/search_result2.png)

### 🌟 Popular Intercity Routes Showcase
![Popular Routes](screenshots/popular_routes.png)

### 🗺️ 28 States & 787 Districts Location Network
![States and District Selection](screenshots/states_and_dist.png)

### 💺 Interactive Real-Time Seat Selection Map (2x2 / 2x1 Sleeper)
![Seat Selection](screenshots/select_seat.png)

### 💳 Passenger Information & Instant Checkout
![Passenger and Card Details](screenshots/Passenger_and_card_details.png)

### ✅ Confirmed e-Ticket Pass with Scannable QR Verification
![Ticket Booked](screenshots/Ticket_booked.png)

### 🖨️ Dedicated Standalone A4 Print View
![Print Ticket](screenshots/print_ticket.png)

### 📄 Commercial Vector PDF e-Ticket Download
![PDF Download](screenshots/pdf_download.png)

### 📊 SaaS Administration Dashboard Overview
![Admin Dashboard](screenshots/Admin_dashboard.png)

### 🛣️ Administrative District Route Management
![Manage Routes](screenshots/manage_route.png)

### 🚍 Bus Fleet & Timetable Dispatch Management
![Manage Buses](screenshots/manage_buses.png)

### 🎛️ Advanced Bus Service Filtering & Sorting Options
![Filter and Sort](screenshots/Filter_and_sort.png)

---

## ✨ Key Features

### 🚌 Passenger Booking Experience
- **Smart Location Network**: Search intercity buses across all **28 Indian States & 787 Districts** with real-time autocompletion and travel date limits.
- **Airline-Style Seat Selection**: Interactive 2D bus interior map displaying driver cabin, entrance door, aisle, and real-time seat states (*Available*, *Booked*, *Selected*). Supports both 2x2 Seater and 2x1 Sleeper layouts.
- **Live Fare Breakdown Engine**: Dynamic fare calculator factoring base ticket prices, 5% GST, and convenience fees.
- **Instant QR e-Ticket Generation**: Base64-encoded encrypted QR verification matrix generated instantly upon payment confirmation.
- **Dual PDF & Print System**:
  - **Native Server PDF (`/ticket/<ref>/pdf`)**: Pure binary vector PDF generation via ReportLab / `xhtml2pdf` optimized for single-page A4 download.
  - **Standalone Print View (`/ticket/<ref>/print`)**: Dedicated print layout using `@media print` and `@page` rules with zero top margin collapse.

### 🛡️ Enterprise & Admin Portal
- **Dashboard Analytics**: Real-time revenue reporting, active booking counters, bus fleet metrics, and route performance insights.
- **Route & Fleet Manager**: Administrative route creator and bus schedule dispatcher supporting custom seat capacities, pricing multipliers, amenities, and timetable pairs.
- **Booking Ledger**: Searchable reservation log showing passenger records, assigned seats, payment statuses, and unique booking reference keys.

### 🎨 Mobile-First UI/UX & Architecture
- **ADS Studio Branding**: Gold-embossed brand identity integrated across header navbar, splash screen, footer, and dedicated About section.
- **Fluid Clamp Typography**: Responsive CSS `clamp()` typography for seamless legibility across all screen sizes.
- **Touch-Friendly Controls**: Minimum 44px tap targets optimized for small mobile viewports (320px) up to 4K desktop displays.
- **Mobile Table Transformations**: Data tables automatically convert to responsive stacked cards on small screens (`data-label`).
- **Toast Notifications**: Built-in interactive alert system for seat selection, route swaps, and input validation feedback.

---

## 🛠️ Technology Stack

| Component | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Backend Core** | Python 3.10+ / Flask 3.0 | Application server, routing, session handling |
| **WSGI Server** | Gunicorn 21.2+ | Production-grade HTTP WSGI server for Cloud / Render |
| **Database** | SQLite3 | Relational data store for 787 districts, routes, buses, seats, & bookings |
| **PDF Generation Engine** | `reportlab` 4.5+ / `xhtml2pdf` 0.2+ | Native server-side commercial vector A4 PDF e-ticket generation |
| **QR Code Engine** | `qrcode` + `Pillow` (PIL) | Dynamic matrix QR code rendering for tickets |
| **Frontend Styling** | Custom CSS3 Custom Properties | Glassmorphism design system, grid, flexbox, clamp() typography |
| **Icons Library** | Lucide Icons (SVG) & Inline SVGs | Lightweight vector icon suite |

---

## 📁 Repository Structure

```text
smart-bus-reservation-system/
├── app.py                  # Main Flask application & WSGI entry point
├── init_db.py              # Database schema initializer (Auto-run on startup)
├── seed_db.py              # Mock data generator (787 Districts, Routes, Buses)
├── india_locations.py      # Comprehensive database of 28 States & 787 Districts
├── Procfile                # Heroku / Render deployment process file
├── render.yaml             # Render Blueprint Infrastructure-as-Code
├── requirements.txt        # Python package dependencies (Flask, ReportLab, etc.)
├── LICENSE                 # Open-source MIT License
├── README.md               # Repository documentation
├── .gitignore              # Ignored files & runtime environment rules
├── screenshots/            # High-resolution application screenshots (16 images)
│   ├── home.png
│   ├── About.png
│   ├── search.png
│   ├── search_result.png
│   ├── search_result2.png
│   ├── popular_routes.png
│   ├── states_and_dist.png
│   ├── select_seat.png
│   ├── Passenger_and_card_details.png
│   ├── Ticket_booked.png
│   ├── print_ticket.png
│   ├── pdf_download.png
│   ├── Admin_dashboard.png
│   ├── manage_route.png
│   ├── manage_buses.png
│   └── Filter_and_sort.png
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
    ├── ticket_print.html   # Standalone A4 print layout & PDF template
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

# (Optional) Seed comprehensive route network across 787 districts
python seed_db.py
```

### Step 5: Launch Application
```bash
python app.py
```

Open your browser and navigate to **`http://127.0.0.1:5050`** (or `http://127.0.0.1:5000`).

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
1. **Search Route**: Select departure district, destination district, date of travel, and preferred bus type on the homepage.
2. **Filter & Select Bus**: Browse available bus services, filter by AC/Sleeper, sort by fare or schedule, and click **Select Seats**.
3. **Choose Seats**: Click available seats on the 2D interactive bus map to review real-time pricing and fare breakdown.
4. **Enter Passenger Info**: Complete full name, age, gender, phone number, and simulated payment credentials.
5. **Receive e-Ticket**: View confirmed e-ticket with scannable QR verification code. Download native A4 PDF or print standalone pass.

### Administrator Flow
1. Navigate to **`/admin`**.
2. **Analytics Overview**: View total bookings, accumulated revenue, active bus fleet count, and registered routes.
3. **Manage Routes**: Add new district-to-district route pairs.
4. **Manage Buses**: Dispatch new bus numbers with custom departure times, seat counts, layout types, and pricing per seat.

---

## 📱 Responsive Screen Compatibility

Tested across all major mobile, tablet, and desktop display resolutions:
- 📱 **Small Mobile (320px – 430px)**: iPhone SE, iPhone 14/15/16 Pro Max, Samsung Galaxy series.
- 📱 **Tablets (768px – 1024px)**: iPad Mini, iPad Air, iPad Pro.
- 💻 **Laptops & Desktops (1280px – 4K)**: MacBook Air/Pro, Windows Laptops, 1440p & 4K Monitors.

---

## 🔮 Future Enhancements Roadmap

- [ ] **Live GPS Tracking**: Integrate real-time bus location tracking via WebSockets.
- [ ] **SMS & WhatsApp Dispatch**: Automated e-ticket notifications via Twilio / WhatsApp API.
- [ ] **Payment Gateway Integration**: Live payment gateway checkout via Razorpay / Stripe.
- [ ] **Multi-Language Support**: i18n support for Hindi, Tamil, Telugu, Marathi, and English.

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
