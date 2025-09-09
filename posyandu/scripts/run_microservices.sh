#!/bin/bash

echo "🚀 Starting Posyandu + Microservices..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "📦 Building and starting all services..."

# Build and start all services
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."

# Wait for database to be ready
sleep 10

# Run migrations for each service
echo "🔄 Running database migrations..."

# Auth Service
echo "  - Auth Service migrations..."
docker-compose exec -T auth-service python manage.py makemigrations
docker-compose exec -T auth-service python manage.py migrate

# Posyandu Service
echo "  - Posyandu Service migrations..."
docker-compose exec -T posyandu-service python manage.py makemigrations
docker-compose exec -T posyandu-service python manage.py migrate


echo "✅ All services are ready!"
echo ""
echo "🌐 Access URLs:"
echo "  - Frontend: http://localhost:3000"
echo "  - API Gateway: http://localhost"
echo "  - Auth Service: http://localhost:8001"
echo "  - Posyandu Service: http://localhost:8002"
echo "  - Anak Service: http://localhost:8003"
echo "  - Penimbangan Service: http://localhost:8004"
echo ""
echo "📊 To view logs:"
echo "  docker-compose logs -f [service-name]"
echo ""
echo "🛑 To stop all services:"
echo "  docker-compose down"
