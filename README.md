# 💰 Finance Manager - Complete App Package

A full-stack personal finance management application with:
- **Python Backend** (SQLite + Flask API)
- **Flutter Mobile App** (Android APK)
- **Web Frontend** (HTML5 + Chart.js)
- **Interactive Charts & Analytics**
- **Product Management & Shopping Cart**
- **Expense & Income Tracking**

## 📦 Package Contents

```
finance_manager_complete/
├── PYTHON_BACKEND/          # Python backend with SQLite
│   ├── finance_app_backend.py    # Core business logic
│   ├── app.py                    # Flask REST API
│   └── requirements.txt           # Python dependencies
│
├── FLUTTER_APP/             # Flutter mobile app
│   ├── pubspec.yaml              # Dependencies
│   ├── lib/main.dart             # Dashboard with charts
│   ├── android/
│   │   ├── app/build.gradle      # Android build config
│   │   └── AndroidManifest.xml   # App manifest
│   └── ...
│
├── WEB_FRONTEND/            # Web application
│   ├── index.html                # Main UI (Chart.js)
│   ├── manifest.json             # PWA configuration
│   ├── service-worker.js         # Offline support
│   └── assets/                   # Icons and images
│
└── DOCUMENTATION/           # Setup guides
    ├── README.md
    ├── SETUP_GUIDE.md
    └── DEPLOY_GUIDE.md
```

## 🚀 Quick Start

### Option 1: Python Backend + Flask API (Recommended)

```bash
# 1. Install Python dependencies
cd PYTHON_BACKEND/
pip install -r requirements.txt

# 2. Run Flask API server
python app.py

# 3. Backend runs on http://localhost:8080
# 4. Frontend served from http://localhost:8080
# 5. Database created: finance_app.db
```

### Option 2: Flutter Mobile App

```bash
# 1. Install Flutter (flutter.dev)
# 2. Navigate to FLUTTER_APP/
cd FLUTTER_APP/

# 3. Get dependencies
flutter pub get

# 4. Run on emulator/device
flutter run

# 5. Build APK
flutter build apk --release

# 6. APK location: build/app/outputs/flutter-apk/app-release.apk
```

### Option 3: Web App (PWA)

```bash
# 1. Deploy WEB_FRONTEND/ folder to:
#    - GitHub Pages
#    - Netlify
#    - Vercel
#    - Any web server

# 2. Go to https://www.pwabuilder.com
# 3. Enter your deployed URL
# 4. Generate APK from PWA
```

## 📱 Features

### Dashboard
- ✅ KPI Cards (Balance, Income, Expenses, Savings Rate)
- ✅ Interactive Charts (Line, Pie, Doughnut, Bar)
- ✅ Financial Summary
- ✅ Monthly Trends

### Products
- ✅ Add/Edit/Delete Products
- ✅ Category Management
- ✅ Inventory Tracking
- ✅ Price Management

### Cart
- ✅ Add/Remove Items
- ✅ Order Summary
- ✅ Checkout Processing
- ✅ Automatic Stock Management

### Expenses
- ✅ Track by Category
- ✅ Filter by Period
- ✅ Payment Method Recording
- ✅ Category-wise Breakdown

### Income
- ✅ Multiple Income Sources
- ✅ Income Type Classification
- ✅ Source-wise Breakdown
- ✅ Period Filtering

### Analytics
- ✅ Financial Summary
- ✅ Expense Breakdown
- ✅ Income Analysis
- ✅ Inventory Value
- ✅ Monthly Trends
- ✅ Top Transactions

## 🗄️ Database Schema

### Products Table
```
id | name | price | quantity | category | description | created_at | updated_at
```

### Expenses Table
```
id | category | amount | description | date | payment_method
```

### Income Table
```
id | source | amount | description | date | income_type
```

### Cart Table
```
id | product_id | quantity | price_at_purchase | added_at
```

## 🔗 API Endpoints

### Dashboard
- `GET /api/dashboard?days=30` - Complete dashboard data
- `GET /api/visualization-data` - Chart data

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create product
- `GET /api/products/<id>` - Get single product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Expenses
- `GET /api/expenses?days=30` - Get expenses
- `POST /api/expenses` - Create expense
- `DELETE /api/expenses/<id>` - Delete expense

### Income
- `GET /api/income?days=30` - Get income
- `POST /api/income` - Create income
- `DELETE /api/income/<id>` - Delete income

### Cart
- `GET /api/cart` - Get cart items
- `POST /api/cart` - Add to cart
- `DELETE /api/cart/<id>` - Remove from cart
- `POST /api/cart/checkout` - Checkout

## 📊 Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.7+ |
| Database | SQLite3 |
| API Server | Flask 2.3+ |
| Frontend (Web) | HTML5, CSS3, JavaScript, Chart.js |
| Frontend (Mobile) | Flutter 3.0+ |
| Charts | fl_chart (Flutter), Chart.js (Web) |
| Storage | SQLite (Backend), localStorage (Web) |

## 📝 Sample Data

App includes 5 sample products, 5 sample expenses, and 2 sample income entries for testing.

## 🔒 Security Notes

- All data stored locally on device
- No external data sharing
- HTTPS recommended for production
- Environment variables in `.env` for sensitive data

## 📦 Deployment

### Backend (Python)
```bash
gunicorn app:app --bind 0.0.0.0:8080
```

### Frontend (Web)
```bash
# Deploy WEB_FRONTEND/ folder to GitHub Pages, Netlify, or Vercel
```

### Mobile (APK)
```bash
# Already compiled in FLUTTER_APP/build/app/outputs/flutter-apk/app-release.apk
```

## 📄 License

MIT License - Free to use and modify

---

**Version:** 1.0.0  
**Created:** December 2025  
**Status:** Production Ready
