#!/bin/bash
# One-command launcher for Calibr8

echo "🚀 Starting Calibr8..."

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "Building Docker image..."
    docker build -t calibr8-app .

    echo "Starting Calibr8 container..."
    docker run --rm -p 8000:8000 \
        -e DEBUG="True" \
        -e GEMINI_API_KEY="${GEMINI_API_KEY}" \
        calibr8-app
else
    echo "Docker not found. Running with Python..."

    # Activate virtual environment if it exists
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    fi

    # Install dependencies
    pip install -r requirements.txt

    # Run migrations
    python manage.py migrate

    # Start server
    echo ""
    echo "✅ Calibr8 is running at http://localhost:8000"
    echo ""
    python manage.py runserver
fi
