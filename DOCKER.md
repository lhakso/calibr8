# Docker Setup for Calibr8

## Quick Start

### Option 1: Using Docker Compose (Recommended)

Run the entire application with PostgreSQL:

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your-api-key-here

# Start the application
docker-compose up --build

# The API will be available at http://localhost:8000/api/
```

To stop:
```bash
docker-compose down
```

To stop and remove all data:
```bash
docker-compose down -v
```

### Option 2: Using Docker Run (Standalone)

Build and run with SQLite (no database container):

```bash
# Build the image
docker build -t calibr8-app .

# Run the container
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DEBUG="True" \
  -e ALLOWED_HOSTS="localhost,127.0.0.1" \
  -e GEMINI_API_KEY="your-gemini-api-key" \
  --name calibr8 \
  calibr8-app

# Check logs
docker logs -f calibr8

# Stop the container
docker stop calibr8

# Remove the container
docker rm calibr8
```

### Option 3: Docker Run with PostgreSQL

```bash
# Create a network
docker network create calibr8-network

# Run PostgreSQL
docker run -d \
  --name calibr8-db \
  --network calibr8-network \
  -e POSTGRES_DB=calibr8db \
  -e POSTGRES_USER=calibr8user \
  -e POSTGRES_PASSWORD=calibr8pass \
  -p 5432:5432 \
  postgres:14

# Build and run the app
docker build -t calibr8-app .

docker run -d \
  --name calibr8 \
  --network calibr8-network \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DEBUG="False" \
  -e ALLOWED_HOSTS="localhost,127.0.0.1" \
  -e GEMINI_API_KEY="your-gemini-api-key" \
  -e AZURE_POSTGRESQL_HOST="calibr8-db" \
  -e AZURE_POSTGRESQL_NAME="calibr8db" \
  -e AZURE_POSTGRESQL_USER="calibr8user" \
  -e AZURE_POSTGRESQL_PASSWORD="calibr8pass" \
  calibr8-app

# Check logs
docker logs -f calibr8
```

## Testing the API

Once running, test the endpoints:

```bash
# List predictions
curl http://localhost:8000/api/predictions/

# Create a prediction
curl -X POST http://localhost:8000/api/predictions/ \
  -H "Content-Type: application/json" \
  -d '{
    "description": "It will rain tomorrow",
    "probability": 0.7,
    "resolve_by": "2025-12-03T00:00:00Z"
  }'

# Get stats
curl http://localhost:8000/api/predictions/stats/

# Get profile
curl http://localhost:8000/api/profile/
```

Or open in browser:
- http://localhost:8000/api/
- http://localhost:8000/api/predictions/
- http://localhost:8000/api/profile/

## Environment Variables

Required:
- `GEMINI_API_KEY` - Your Google Gemini API key

Optional:
- `SECRET_KEY` - Django secret key (auto-generated if not provided)
- `DEBUG` - Set to "True" for development, "False" for production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

For PostgreSQL:
- `AZURE_POSTGRESQL_HOST` - Database hostname
- `AZURE_POSTGRESQL_NAME` - Database name
- `AZURE_POSTGRESQL_USER` - Database user
- `AZURE_POSTGRESQL_PASSWORD` - Database password

## Development with Docker

Mount your code as a volume for live reloading:

```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd):/app \
  -e DEBUG="True" \
  -e GEMINI_API_KEY="your-key" \
  --name calibr8-dev \
  calibr8-app
```

## Troubleshooting

### Check container logs:
```bash
docker logs -f calibr8
```

### Access container shell:
```bash
docker exec -it calibr8 bash
```

### Run migrations manually:
```bash
docker exec -it calibr8 python manage.py migrate
```

### Create superuser:
```bash
docker exec -it calibr8 python manage.py createsuperuser
```

### Rebuild after changes:
```bash
docker-compose down
docker-compose up --build
```
