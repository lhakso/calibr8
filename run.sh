#!/bin/bash

echo "Starting Calibr8 Web Version..."
echo ""
echo "1. Starting Django backend on http://localhost:8000"
python manage.py runserver &
DJANGO_PID=$!

echo "2. Starting frontend server on http://localhost:8080"
cd frontend
python -m http.server 8080 &
FRONTEND_PID=$!

echo ""
echo "✅ Calibr8 is running!"
echo ""
echo "Backend API:  http://localhost:8000/api/"
echo "Frontend App: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $DJANGO_PID $FRONTEND_PID; exit" INT
wait
