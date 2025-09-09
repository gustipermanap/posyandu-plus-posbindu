#!/bin/bash

# Script untuk setup dan testing semua services Posyandu

echo "🚀 Setting up Posyandu Microservices..."

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Run migrations for each service
echo "📊 Running migrations..."

# Auth Service
echo "  - Auth Service migrations..."
docker-compose exec auth-service python manage.py makemigrations
docker-compose exec auth-service python manage.py migrate

# Posyandu Service
echo "  - Posyandu Service migrations..."
docker-compose exec posyandu-service python manage.py makemigrations
docker-compose exec posyandu-service python manage.py migrate

# Balita Service
echo "  - Balita Service migrations..."
docker-compose exec balita-service python manage.py makemigrations
docker-compose exec balita-service python manage.py migrate

# Ibu Hamil Service
echo "  - Ibu Hamil Service migrations..."
docker-compose exec ibu-hamil-service python manage.py makemigrations
docker-compose exec ibu-hamil-service python manage.py migrate

# Imunisasi Service
echo "  - Imunisasi Service migrations..."
docker-compose exec imunisasi-service python manage.py makemigrations
docker-compose exec imunisasi-service python manage.py migrate

# KB Service
echo "  - KB Service migrations..."
docker-compose exec kb-service python manage.py makemigrations
docker-compose exec kb-service python manage.py migrate

# Vitamin Service
echo "  - Vitamin Service migrations..."
docker-compose exec vitamin-service python manage.py makemigrations
docker-compose exec vitamin-service python manage.py migrate

# Rujukan Service
echo "  - Rujukan Service migrations..."
docker-compose exec rujukan-service python manage.py makemigrations
docker-compose exec rujukan-service python manage.py migrate

# Laporan Service
echo "  - Laporan Service migrations..."
docker-compose exec laporan-service python manage.py makemigrations
docker-compose exec laporan-service python manage.py migrate

# Create superuser for auth service
echo "👤 Creating superuser..."
docker-compose exec auth-service python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@posyandu.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Test API endpoints
echo "🧪 Testing API endpoints..."

# Test Auth Service
echo "  - Testing Auth Service..."
curl -s http://localhost:8001/api/auth/health/ || echo "Auth Service not responding"

# Test Posyandu Service
echo "  - Testing Posyandu Service..."
curl -s http://localhost:8002/api/posyandu/ || echo "Posyandu Service not responding"

# Test Balita Service
echo "  - Testing Balita Service..."
curl -s http://localhost:8003/api/balita/ || echo "Balita Service not responding"

# Test Ibu Hamil Service
echo "  - Testing Ibu Hamil Service..."
curl -s http://localhost:8004/api/ibu-hamil/ || echo "Ibu Hamil Service not responding"

# Test Imunisasi Service
echo "  - Testing Imunisasi Service..."
curl -s http://localhost:8005/api/imunisasi/ || echo "Imunisasi Service not responding"

# Test KB Service
echo "  - Testing KB Service..."
curl -s http://localhost:8006/api/kb/ || echo "KB Service not responding"

# Test Vitamin Service
echo "  - Testing Vitamin Service..."
curl -s http://localhost:8007/api/vitamin/ || echo "Vitamin Service not responding"

# Test Rujukan Service
echo "  - Testing Rujukan Service..."
curl -s http://localhost:8008/api/rujukan/ || echo "Rujukan Service not responding"

# Test Laporan Service
echo "  - Testing Laporan Service..."
curl -s http://localhost:8009/api/laporan/ || echo "Laporan Service not responding"

# Test API Gateway
echo "  - Testing API Gateway..."
curl -s http://localhost:80/health || echo "API Gateway not responding"

echo "✅ Setup completed!"
echo ""
echo "🌐 Services are running:"
echo "  - Frontend: http://localhost:3000"
echo "  - API Gateway: http://localhost:80"
echo "  - Auth Service: http://localhost:8001"
echo "  - Posyandu Service: http://localhost:8002"
echo "  - Balita Service: http://localhost:8003"
echo "  - Ibu Hamil Service: http://localhost:8004"
echo "  - Imunisasi Service: http://localhost:8005"
echo "  - KB Service: http://localhost:8006"
echo "  - Vitamin Service: http://localhost:8007"
echo "  - Rujukan Service: http://localhost:8008"
echo "  - Laporan Service: http://localhost:8009"
echo ""
echo "👤 Admin credentials: admin/admin123"
echo ""
echo "📊 To view logs: docker-compose logs -f [service-name]"
echo "🛑 To stop: docker-compose down"
