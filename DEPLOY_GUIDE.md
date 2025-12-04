# 🛠️ Setup & Installation Guide

## Prerequisites

- Python 3.7 or higher
- Flutter SDK (for mobile app)
- Android Studio (for Android development)
- Git (optional, for version control)
- 500MB free disk space

## Step-by-Step Installation

### Step 1: Python Backend Setup

```bash
# Navigate to PYTHON_BACKEND directory
cd PYTHON_BACKEND

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test backend
python finance_app_backend.py
```

### Step 2: Flask API Server

```bash
# Still in PYTHON_BACKEND directory
# Run Flask app
python app.py

# Server runs on http://localhost:8080
# Open browser and go to http://localhost:8080
```

### Step 3: Flutter Mobile App (Optional)

```bash
# Install Flutter
# Download from: https://flutter.dev/docs/get-started/install

# Verify Flutter installation
flutter doctor

# Navigate to FLUTTER_APP directory
cd FLUTTER_APP

# Get Flutter dependencies
flutter pub get

# Run on connected device/emulator
flutter run

# Build APK
flutter build apk --release
```

## Database Setup

Database automatically created on first run with tables:
- `products` - Product inventory
- `expenses` - Expense records
- `income` - Income records
- `cart` - Shopping cart items
- `transactions` - Completed purchases

## Port Configuration

| Component | Default Port | Environment Variable |
|-----------|--------------|----------------------|
| Flask API | 8080 | API_PORT |
| Flutter | Device specific | N/A |
| Web App | 80/443 | Depends on host |

## Testing

### Test Backend API

```bash
# Using curl
curl http://localhost:8080/api/health

# Expected response:
{"status": "healthy", "message": "..."}
```

### Test Frontend

```bash
# Open in browser
http://localhost:8080/

# Check console for errors
# Press F12 to open developer tools
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8080
# Windows:
netstat -ano | findstr :8080
# macOS/Linux:
lsof -i :8080

# Kill process
kill -9 <PID>
```

### Database Lock Error

```bash
# Delete corrupted database and restart
rm finance_app.db
python app.py
```

### Flutter Build Issues

```bash
# Clean Flutter cache
flutter clean

# Get dependencies again
flutter pub get

# Rebuild
flutter build apk --release
```

## Next Steps

1. Backend running - Verify at http://localhost:8080/api/health
2. Frontend loaded - Check dashboard displays data
3. Add test data - Use modals to add products/expenses
4. Test checkout - Try purchasing items
5. Build APK - Follow DEPLOY_GUIDE.md
