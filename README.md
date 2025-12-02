# 🎯 Calibr8: Prediction Tracking & Calibration Analysis

A full-stack web application for tracking predictions and improving calibration using Django REST Framework, Google Gemini AI, and javascript, css frontend. Deployed on Azure with full containerization support.

---

## 1) Executive Summary

### Problem
A few weeks ago I had watched a video on how people make predictions constantly in daily life and professional settings, but rarely track their accuracy or learn from their mistakes. This leads to overconfidence, poor decision-making, and a lack of awareness. I wanted a way to track my own predictions, see how well-calibrated I am, and get insights on how to improve.

### Solution
Calibr8 is a web-based prediction tracking platform that allows users to:
- Record predictions with confidence levels (0-100%)
- Mark predictions as resolved with actual outcomes
- Analyze calibration quality through Brier scores and visual calibration charts
- Track historical performance and identify areas for improvement

The system provides immediate feedback on calibration quality, helping users become better forecasters through quantitative analysis and personalized AI recommendations.

---

## 2) System Overview

### Course Concepts

**Django REST Framework** - I've built several Django apps before, so this made sense. Uses ViewSets for CRUD operations and custom actions for domain logic like calculating Brier scores.

**LLM Integration** - Google Gemini API generates insights about calibration patterns and suggests improvements to predictions.

**Docker** - Fully containerized with support for both SQLite (dev) and PostgreSQL (production).

**Cloud Deployment** - Deployed on Azure App Service with GitHub auto-deployment.

### Architecture Diagram

![Architecture Diagram](assets/arch.png)

### Data Models & Services

**Models:**
- `Prediction`: UUID primary key, description (text), probability (0.0-1.0), timestamps, optional resolve_by date, resolved status, outcome boolean
- `UserProfile`: Name and notes fields for user customization

**External Services:**
- Google Gemini API (gemini-2.5-flash-lite-preview-09-2025) for AI insights
- No external datasets - all user-generated data

---

## 3) How to Run (Local)

### Prerequisites
- Docker installed OR Python 3.13+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/lhakso/calibr8.git
cd calibr8

# Set your Gemini API key
export GEMINI_API_KEY="your-api-key-here"

# Build and run
docker build -t calibr8-app .
docker run --rm -p 8000:8000 \
  -e DEBUG="True" \
  -e GEMINI_API_KEY="${GEMINI_API_KEY}" \
  calibr8-app

# Access the app
open http://localhost:8000
```

### Option 2: Using run.sh

```bash
# Make sure script is executable
chmod +x run.sh

# Set API key
export GEMINI_API_KEY="your-api-key-here"

# Run (automatically detects Docker or falls back to Python)
./run.sh
```

### Option 3: Python Virtual Environment

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

# Access at http://localhost:8000
```

### Health Check

```bash
# Test API endpoints
curl http://localhost:8000/api/predictions/
curl http://localhost:8000/api/profile/

# Run automated tests
cd tests
pip install -r requirements.txt
python test_api.py
```

### Docker Compose (with PostgreSQL)

```bash
# Start full stack with database
docker-compose up --build

# Access at http://localhost:8000
```

---

## 4) Design Decisions

### Why These Choices?

**Django** - I've built multiple Django apps already, so I'm comfortable with it. DRF makes REST APIs really easy.

**Gemini** - Better free tier than OpenAI. Works well for this kind of analytical task.

**Vanilla JS** - Didn't need React for something this small. Keeps it simple.

**Docker** - Makes deployment consistent. Same container works locally and in production.

### Tradeoffs

**Performance** - SQLite works fine for single-user but wouldn't scale. That's why PostgreSQL is an option for Azure.

**Complexity** - Kept it simple - no Redis, no Celery, no build system. Just what's needed.

**Cost** - Azure runs about $25/month (without PostgreSQL it's just for the app service).

### Security

- API keys in environment variables only (`.env.example` template, actual keys never committed)
- DRF serializers validate inputs
- CSRF protection enabled
- No auth yet (single-user app)

### Limitations

- No real-time updates
- Single timezone (UTC)
- SQLite data on Azure resets when the app restarts

---

## 5) Results & Evaluation

### What Works

- Create predictions with confidence sliders
- Click to resolve (happened/didn't happen)
- View Brier score and calibration charts
- AI suggestions for prediction wording
- AI analysis of calibration patterns

### Performance

- Container: ~450MB, builds in 2-3 minutes
- API responses: <100ms
- AI insights: 1-3 seconds
- Handles hundreds of predictions fine

### Testing

Automated tests cover creating, resolving, stats, and profile management. All CRUD operations tested. Manually tested on Chrome.

---

## 6) What's Next

**Features I'd like to add:**
- Data export (JSON/CSV)
- Prediction categories and tags
- Email reminders for unresolved predictions
- Historical performance graphs

**Technical improvements:**
- Add authentication for multi-user support
- Rate limiting on AI endpoints
- Redis for caching stats
- GitHub Actions CI/CD
- Automated database backups

---

## 7) Links (Required)

- **GitHub Repository:** https://github.com/lhakso/calibr8
- **Public Cloud App:** https://calibr8-app.azurewebsites.net

---

## License & Credits

MIT License. Uses Django REST Framework (BSD), Google Generative AI (Apache 2.0), and vanilla JavaScript.

---

**Built for better decision-making through systematic calibration tracking.**
