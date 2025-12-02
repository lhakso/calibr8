# Calibr8 - Web Application

A prediction tracking app with calibration analysis, built with Django backend and Vanilla JavaScript frontend.

## Project Structure

```
calibr8/
├── backend/                    # Django project settings
│   ├── settings.py             # Django config with CORS, REST framework
│   └── urls.py                 # Main URL routing
│
├── predictions/                # Django app
│   ├── models.py               # Prediction & UserProfile models
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # API endpoints + stats calculations
│   ├── urls.py                 # API routes
│   └── admin.py                # Django admin config
│
├── frontend/                   # Web frontend
│   ├── index.html              # Main HTML with tabs
│   ├── styles.css              # Clean Apple-inspired design
│   └── app.js                  # API integration & UI logic
│
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
├── run.sh                      # Quick start script
└── PROJECT_OVERVIEW.md         # This file
```

## Features

The web application implements:

1. **Add Predictions**
   - Description text
   - Probability slider (0-100%)
   - Optional resolve-by date

2. **View Predictions**
   - Active predictions (unresolved)
   - Resolved predictions (with outcomes)

3. **Resolve Predictions**
   - Mark as "Happened" or "Didn't Happen"

4. **Statistics**
   - Brier score calculation
   - Calibration bins (10% ranges)
   - Visual breakdown

5. **User Profile**
   - Name
   - Notes about goals/life

## Django Backend API

### Endpoints

**Predictions:**
- `GET /api/predictions/` - List all
- `POST /api/predictions/` - Create new
- `GET /api/predictions/{id}/` - Get one
- `PATCH /api/predictions/{id}/` - Update
- `DELETE /api/predictions/{id}/` - Delete
- `POST /api/predictions/{id}/resolve/` - Mark outcome
- `GET /api/predictions/stats/` - Get Brier score & bins

**Profile:**
- `GET /api/profile/` - Get profile
- `PATCH /api/profile/1/` - Update profile

### Stats Calculation

The backend calculates:

**Brier Score:**
```python
brier_score = average((probability - outcome)^2)
```

**Calibration Bins:**
- Groups predictions into 10% ranges
- Requires min 3 predictions per bin
- Compares avg predicted vs actual frequency

## Running the Project

```bash
# Start both servers
./run.sh

# Or manually:
python manage.py runserver          # Backend on :8000
cd frontend && python -m http.server 8080  # Frontend on :8080
```

Visit: http://localhost:8080

## Data Models

### Prediction
```python
id: UUID
description: String/TextField
probability: Float (0.0-1.0)
created_at: DateTime
resolve_by: DateTime (optional)
resolved: Boolean
outcome: Boolean (optional)
```

### UserProfile
```python
id: Integer
name: String
notes: TextField
```

## Design Philosophy

**Clean & Simple:**
- Apple-inspired design language
- Focus on usability over features
- Clear visual hierarchy
- Responsive layout

**Educational:**
- Helps users learn about calibration
- Visual feedback on prediction accuracy
- Encourages metacognitive awareness

## Future Enhancements

- [ ] LLM integration for personalized insights
- [ ] Daily suggested predictions based on profile
- [ ] Charts/graphs for calibration visualization
- [ ] Export data (CSV, JSON)
- [ ] Social features (compare with friends)
- [ ] Prediction categories/tags
- [ ] Dark mode

## Tech Stack

**Frontend:**
- HTML5
- CSS3 (Flexbox, Grid)
- Vanilla JavaScript (ES6+)
- Fetch API

**Backend:**
- Django 5.2
- Django REST Framework
- SQLite
- django-cors-headers

**Dev Tools:**
- uv (Python package manager)
- Git (version control)

## Key Concepts

This project demonstrates:

1. **Full-stack web development** - Backend API + frontend
2. **RESTful API design** - Proper HTTP methods and endpoints
3. **State management** - Vanilla JavaScript patterns
4. **Data persistence** - SQLite database
5. **Statistical algorithms** - Brier score, calibration analysis
6. **UI/UX design** - Clean, intuitive interfaces
