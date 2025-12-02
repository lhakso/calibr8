# Calibr8 Web Version

Django backend + vanilla JS frontend for testing Calibr8 locally without Xcode.

## Quick Start

### 1. Start the Django Backend

```bash
# Run migrations (already done)
python manage.py migrate

# Start the server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

### 2. Open the Frontend

Simply open `frontend/index.html` in your browser, or use a simple server:

```bash
cd frontend
python -m http.server 8080
```

Then visit `http://localhost:8080`

## API Endpoints

The Django backend provides these REST endpoints:

### Predictions
- `GET /api/predictions/` - List all predictions
- `POST /api/predictions/` - Create new prediction
- `GET /api/predictions/{id}/` - Get single prediction
- `PATCH /api/predictions/{id}/` - Update prediction
- `DELETE /api/predictions/{id}/` - Delete prediction
- `POST /api/predictions/{id}/resolve/` - Resolve prediction with outcome
- `GET /api/predictions/stats/` - Get Brier score and calibration bins

### Profile
- `GET /api/profile/` - Get user profile
- `PATCH /api/profile/1/` - Update user profile

## Features

**Web Frontend:**
- Add predictions with probability slider
- Optional resolve-by dates
- Resolve predictions as happened/didn't happen
- View statistics (Brier score, calibration bins)
- User profile

**Django Backend:**
- RESTful API
- SQLite database
- Same business logic as iOS app
- Stats calculations (Brier score, calibration bins)

## Architecture

```
Web App (frontend/index.html)
    ↓
Django REST API (http://localhost:8000/api/)
    ↓
SQLite Database (db.sqlite3)
```

## Testing the API Directly

You can test the API with curl:

```bash
# Get all predictions
curl http://localhost:8000/api/predictions/

# Create a prediction
curl -X POST http://localhost:8000/api/predictions/ \
  -H "Content-Type: application/json" \
  -d '{"description": "I will finish my project on time", "probability": 0.7}'

# Get stats
curl http://localhost:8000/api/predictions/stats/
```

## Next Steps

- The iOS app can connect to this same backend API
- You can develop the web version first, then build the iOS app
- Both will share the same backend logic and data
