#!/bin/bash

# =============================================================================
# Setup Docker untuk Development Posyandu + Microservices
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Docker status
check_docker() {
    print_status "Checking Docker installation..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        print_status "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "Docker is installed and running"
}

# Function to check Docker Compose
check_docker_compose() {
    print_status "Checking Docker Compose..."
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        print_status "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_success "Docker Compose is available"
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    # Create mediafiles directory if not exists
    mkdir -p mediafiles/profile_pics
    mkdir -p logs
    
    # Create .env file if not exists
    if [ ! -f .env ]; then
        print_status "Creating .env file from env.example..."
        if [ -f env.example ]; then
            cp env.example .env
            print_success ".env file created"
        else
            print_warning "env.example not found, creating basic .env file..."
            cat > .env << EOF
# Database Configuration
POSTGRES_DB=posyandu_shared
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=shared-database
POSTGRES_PORT=5432

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# API Gateway
API_GATEWAY_URL=http://localhost
FRONTEND_URL=http://localhost:3000
EOF
            print_success "Basic .env file created"
        fi
    fi
    
    print_success "Directories created successfully"
}

# Function to pull base images
pull_base_images() {
    print_status "Pulling base Docker images..."
    
    # Pull PostgreSQL image
    docker pull postgres:15-alpine
    
    # Pull Python image
    docker pull python:3.11-slim
    
    # Pull Node.js image for frontend
    docker pull node:18-alpine
    
    # Pull Nginx image
    docker pull nginx:alpine
    
    print_success "Base images pulled successfully"
}

# Function to build custom images
build_custom_images() {
    print_status "Building custom Docker images..."
    
    # Build all services
    docker-compose build --no-cache
    
    print_success "Custom images built successfully"
}

# Function to setup database
setup_database() {
    print_status "Setting up database..."
    
    # Start only database first
    docker-compose up -d shared-database
    
    # Wait for database to be ready
    print_status "Waiting for database to be ready..."
    sleep 15
    
    # Create databases for each service
    print_status "Creating databases for each service..."
    
    databases=(
        "posyandu_auth"
        "posyandu_posyandu"
        "posyandu_balita"
        "posyandu_ibu_hamil"
        "posyandu_imunisasi"
        "posyandu_kb"
        "posyandu_vitamin"
        "posyandu_rujukan"
        "posyandu_laporan"
    )
    
    for db in "${databases[@]}"; do
        print_status "Creating database: $db"
        docker-compose exec -T shared-database psql -U postgres -c "CREATE DATABASE $db;" || true
    done
    
    print_success "Database setup completed"
}

# Function to run migrations
run_migrations() {
    print_status "Running database migrations..."
    
    # Start all services
    docker-compose up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 20
    
    # Run migrations for each service
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
        docker-compose exec -T $service python manage.py makemigrations || true
        docker-compose exec -T $service python manage.py migrate || true
    done
    
    print_success "Migrations completed"
}

# Function to create superuser
create_superuser() {
    print_status "Creating superuser..."
    
    # Create superuser for auth service
    docker-compose exec -T auth-service python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@posyandu.com', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF
    
    print_success "Superuser created"
}

# Function to verify setup
verify_setup() {
    print_status "Verifying setup..."
    
    # Check if all services are running
    services=(
        "shared-database"
        "auth-service"
        "posyandu-service"
        "balita-service"
        "ibu-hamil-service"
        "imunisasi-service"
        "kb-service"
        "vitamin-service"
        "rujukan-service"
        "laporan-service"
        "api-gateway"
        "frontend"
    )
    
    for service in "${services[@]}"; do
        if docker-compose ps | grep -q "$service.*Up"; then
            print_success "$service is running"
        else
            print_error "$service is not running"
        fi
    done
    
    # Test API endpoints
    print_status "Testing API endpoints..."
    
    # Test auth service
    if curl -s http://localhost:8001/api/auth/ >/dev/null; then
        print_success "Auth service API is accessible"
    else
        print_warning "Auth service API is not accessible"
    fi
    
    # Test API gateway
    if curl -s http://localhost/ >/dev/null; then
        print_success "API Gateway is accessible"
    else
        print_warning "API Gateway is not accessible"
    fi
    
    # Test frontend
    if curl -s http://localhost:3000/ >/dev/null; then
        print_success "Frontend is accessible"
    else
        print_warning "Frontend is not accessible"
    fi
}

# Function to show access information
show_access_info() {
    echo ""
    echo "============================================================================="
    echo "🎉 Docker Setup Completed Successfully!"
    echo "============================================================================="
    echo ""
    echo "🌐 Access URLs:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - API Gateway: http://localhost"
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
    echo "🔑 Login Credentials:"
    echo "  - Username: admin"
    echo "  - Password: admin123"
    echo ""
    echo "📊 Useful Commands:"
    echo "  - View logs: docker-compose logs -f [service-name]"
    echo "  - Stop all: docker-compose down"
    echo "  - Restart: docker-compose restart [service-name]"
    echo "  - Shell access: docker-compose exec [service-name] bash"
    echo ""
    echo "============================================================================="
}

# Main execution
main() {
    echo "============================================================================="
    echo "🐳 Setting up Docker for Posyandu + Microservices Development"
    echo "============================================================================="
    echo ""
    
    # Check prerequisites
    check_docker
    check_docker_compose
    
    # Setup
    create_directories
    pull_base_images
    build_custom_images
    setup_database
    run_migrations
    create_superuser
    
    # Verify and show info
    verify_setup
    show_access_info
    
    print_success "Docker setup completed successfully!"
}

# Run main function
main "$@"
