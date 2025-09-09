#!/bin/bash

# Setup POS BINDU PTM Microservices
echo "🚀 Setting up POS BINDU PTM Microservices"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Run migrations for each service
echo "📊 Running database migrations..."

# Participant Service
echo "  - Participant Service migrations..."
docker-compose exec participant-service python manage.py makemigrations
docker-compose exec participant-service python manage.py migrate

# Screening Service
echo "  - Screening Service migrations..."
docker-compose exec screening-service python manage.py makemigrations
docker-compose exec screening-service python manage.py migrate

# Examination Service
echo "  - Examination Service migrations..."
docker-compose exec examination-service python manage.py makemigrations
docker-compose exec examination-service python manage.py migrate

# Lab Service
echo "  - Lab Service migrations..."
docker-compose exec lab-service python manage.py makemigrations
docker-compose exec lab-service python manage.py migrate

# Risk Assessment Service
echo "  - Risk Assessment Service migrations..."
docker-compose exec risk-assessment-service python manage.py makemigrations
docker-compose exec risk-assessment-service python manage.py migrate

# Intervention Service
echo "  - Intervention Service migrations..."
docker-compose exec intervention-service python manage.py makemigrations
docker-compose exec intervention-service python manage.py migrate

# Referral Service
echo "  - Referral Service migrations..."
docker-compose exec referral-service python manage.py makemigrations
docker-compose exec referral-service python manage.py migrate

# Reporting Service
echo "  - Reporting Service migrations..."
docker-compose exec reporting-service python manage.py makemigrations
docker-compose exec reporting-service python manage.py migrate

# Test services
echo "🧪 Testing services..."

# Test Participant Service
echo "  - Testing Participant Service..."
curl -s http://localhost:8005/api/participant/ || echo "Participant Service not responding"

# Test Screening Service
echo "  - Testing Screening Service..."
curl -s http://localhost:8006/api/screening/ || echo "Screening Service not responding"

# Test Examination Service
echo "  - Testing Examination Service..."
curl -s http://localhost:8007/api/examination/ || echo "Examination Service not responding"

# Test Lab Service
echo "  - Testing Lab Service..."
curl -s http://localhost:8008/api/lab/ || echo "Lab Service not responding"

# Test Risk Assessment Service
echo "  - Testing Risk Assessment Service..."
curl -s http://localhost:8009/api/risk-assessment/ || echo "Risk Assessment Service not responding"

# Test Intervention Service
echo "  - Testing Intervention Service..."
curl -s http://localhost:8010/api/intervention/ || echo "Intervention Service not responding"

# Test Referral Service
echo "  - Testing Referral Service..."
curl -s http://localhost:8011/api/referral/ || echo "Referral Service not responding"

# Test Reporting Service
echo "  - Testing Reporting Service..."
curl -s http://localhost:8012/api/reporting/ || echo "Reporting Service not responding"

# Test API Gateway
echo "  - Testing API Gateway..."
curl -s http://localhost:8080/health || echo "API Gateway not responding"

echo "✅ Setup completed!"
echo ""
echo "🌐 Services are running:"
echo "  - Frontend: http://localhost:3001"
echo "  - API Gateway: http://localhost:8080"
echo "  - Participant Service: http://localhost:8005"
echo "  - Screening Service: http://localhost:8006"
echo "  - Examination Service: http://localhost:8007"
echo "  - Lab Service: http://localhost:8008"
echo "  - Risk Assessment Service: http://localhost:8009"
echo "  - Intervention Service: http://localhost:8010"
echo "  - Referral Service: http://localhost:8011"
echo "  - Reporting Service: http://localhost:8012"
echo ""
echo "📊 To view logs: docker-compose logs -f [service-name]"
echo "🛑 To stop: docker-compose down"
