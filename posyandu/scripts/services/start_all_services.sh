#!/bin/bash

# =============================================================================
# Script: Start All Posyandu+ Services
# Description: Start semua Posyandu+ microservices menggunakan Docker Compose
# Author: Posyandu+ Development Team
# Version: 1.0
# =============================================================================

set -e

# Colors untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function untuk print dengan warna
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function untuk menampilkan help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --no-migrations    Skip database migrations"
    echo "  --quick           Quick start (skip health checks)"
    echo "  --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                 # Start semua services dengan migrations"
    echo "  $0 --no-migrations # Start tanpa migrations"
    echo "  $0 --quick         # Quick start"
}

# Parse arguments
SKIP_MIGRATIONS=false
QUICK_START=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --no-migrations)
            SKIP_MIGRATIONS=true
            shift
            ;;
        --quick)
            QUICK_START=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml not found. Please run this script from the project root."
    exit 1
fi

print_status "Starting Posyandu+ Services..."

# Start services
if [ "$QUICK_START" = true ]; then
    print_status "Quick start mode - starting services without health checks..."
    docker-compose up -d
else
    print_status "Starting services with health checks..."
    docker-compose up -d --wait
fi

# Wait for services to be ready
if [ "$QUICK_START" = false ]; then
    print_status "Waiting for services to be ready..."
    sleep 10
fi

# Run migrations if not skipped
if [ "$SKIP_MIGRATIONS" = false ]; then
    print_status "Running database migrations..."
    
    # List of services that need migrations
    services=(
        "auth-service"
        "posyandu-service"
        "balita-service"
        "ibu-hamil-service"
        "imunisasi-service"
        "kb-service"
        "vitamin-service"
        "rujukan-service"
        "laporan-service"
    )
    
    for service in "${services[@]}"; do
        print_status "Running migrations for $service..."
        if docker-compose exec -T "$service" python manage.py migrate --noinput; then
            print_success "Migrations completed for $service"
        else
            print_warning "Failed to run migrations for $service"
        fi
    done
else
    print_warning "Skipping database migrations"
fi

# Check service status
print_status "Checking service status..."
docker-compose ps

# Show access URLs
echo ""
print_success "Posyandu+ Services started successfully!"
echo ""
echo "🌐 Access URLs:"
echo "  Frontend:     http://localhost:3000"
echo "  API Gateway:  http://localhost"
echo "  Auth Service: http://localhost:8001"
echo ""
echo "🔑 Default Login:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "📊 To monitor services:"
echo "  docker-compose logs -f"
echo "  docker-compose ps"
echo ""
