#!/bin/bash

# =============================================================================
# Restart Individual Posyandu + Microservice
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_header() {
    echo -e "${PURPLE}[HEADER]${NC} $1"
}

# Available services
AVAILABLE_SERVICES=(
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

# Service ports
declare -A SERVICE_PORTS=(
    ["shared-database"]="5432"
    ["auth-service"]="8001"
    ["posyandu-service"]="8002"
    ["balita-service"]="8003"
    ["ibu-hamil-service"]="8004"
    ["imunisasi-service"]="8005"
    ["kb-service"]="8006"
    ["vitamin-service"]="8007"
    ["rujukan-service"]="8008"
    ["laporan-service"]="8009"
    ["api-gateway"]="80"
    ["frontend"]="3000"
)

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to validate service name
validate_service() {
    local service_name="$1"
    
    for service in "${AVAILABLE_SERVICES[@]}"; do
        if [ "$service" = "$service_name" ]; then
            return 0
        fi
    done
    
    return 1
}

# Function to restart service
restart_service() {
    local service_name="$1"
    local port="${SERVICE_PORTS[$service_name]}"
    
    print_header "Restarting $service_name..."
    
    # Check if service is running
    if docker-compose ps | grep -q "$service_name.*Up"; then
        print_status "Stopping $service_name..."
        docker-compose stop "$service_name"
    else
        print_warning "Service $service_name is not currently running"
    fi
    
    # Start the service
    print_status "Starting $service_name..."
    docker-compose up -d "$service_name"
    
    # Wait for service to be ready
    if [ -n "$port" ]; then
        print_status "Waiting for $service_name to be ready on port $port..."
        sleep 5
        
        # Check if service is accessible
        if [ "$service_name" = "shared-database" ]; then
            # For database, just wait
            print_success "$service_name is starting up"
        else
            # For other services, try to check if they're accessible
            local max_attempts=30
            local attempt=0
            
            while [ $attempt -lt $max_attempts ]; do
                if docker-compose exec -T "$service_name" curl -s http://localhost:$port/ >/dev/null 2>&1 || \
                   docker-compose exec -T "$service_name" nc -z localhost $port >/dev/null 2>&1; then
                    print_success "$service_name is ready and accessible"
                    break
                fi
                sleep 2
                attempt=$((attempt + 1))
            done
            
            if [ $attempt -eq $max_attempts ]; then
                print_warning "$service_name may not be fully ready yet"
            fi
        fi
    fi
}

# Function to run migrations for service
run_migrations() {
    local service_name="$1"
    
    # Only run migrations for Django services (not database, api-gateway, or frontend)
    if [[ "$service_name" == *"-service" ]] && [ "$service_name" != "api-gateway" ]; then
        print_status "Running migrations for $service_name..."
        docker-compose exec -T "$service_name" python manage.py makemigrations || true
        docker-compose exec -T "$service_name" python manage.py migrate || true
        print_success "Migrations completed for $service_name"
    fi
}

# Function to show service status
show_service_status() {
    local service_name="$1"
    
    print_header "Service Status:"
    echo ""
    docker-compose ps "$service_name"
    echo ""
}

# Function to show service information
show_service_info() {
    local service_name="$1"
    local port="${SERVICE_PORTS[$service_name]}"
    
    echo ""
    echo "============================================================================="
    echo "🔄 Service $service_name Restarted Successfully!"
    echo "============================================================================="
    echo ""
    echo "🌐 Access Information:"
    if [ -n "$port" ]; then
        if [ "$service_name" = "shared-database" ]; then
            echo "  - Database: localhost:$port"
            echo "  - Connection: postgresql://postgres:password@localhost:$port"
        elif [ "$service_name" = "api-gateway" ]; then
            echo "  - API Gateway: http://localhost"
        elif [ "$service_name" = "frontend" ]; then
            echo "  - Frontend: http://localhost:$port"
        else
            echo "  - Service URL: http://localhost:$port"
            echo "  - API Endpoint: http://localhost:$port/api/"
        fi
    fi
    echo ""
    echo "📊 Useful Commands:"
    echo "  - View logs: docker-compose logs -f $service_name"
    echo "  - Stop service: docker-compose stop $service_name"
    echo "  - Restart service: docker-compose restart $service_name"
    echo "  - Shell access: docker-compose exec $service_name bash"
    echo "  - View status: docker-compose ps $service_name"
    echo ""
    echo "============================================================================="
}

# Function to show help
show_help() {
    echo "Usage: $0 SERVICE_NAME [OPTIONS]"
    echo ""
    echo "Available Services:"
    for service in "${AVAILABLE_SERVICES[@]}"; do
        local port="${SERVICE_PORTS[$service]}"
        echo "  - $service (port: $port)"
    done
    echo ""
    echo "Options:"
    echo "  --no-migrations    Skip database migrations"
    echo "  --status           Show service status only"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 auth-service"
    echo "  $0 balita-service --no-migrations"
    echo "  $0 frontend --status"
}

# Main execution
main() {
    echo "============================================================================="
    echo "🔄 Restarting Individual Posyandu + Microservice"
    echo "============================================================================="
    echo ""
    
    # Check prerequisites
    check_docker
    
    # Parse command line arguments
    SERVICE_NAME=""
    NO_MIGRATIONS=false
    STATUS_ONLY=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-migrations)
                NO_MIGRATIONS=true
                shift
                ;;
            --status)
                STATUS_ONLY=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            -*)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                if [ -z "$SERVICE_NAME" ]; then
                    SERVICE_NAME="$1"
                else
                    print_error "Multiple service names provided"
                    show_help
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Check if service name is provided
    if [ -z "$SERVICE_NAME" ]; then
        print_error "Service name is required"
        show_help
        exit 1
    fi
    
    # Validate service name
    if ! validate_service "$SERVICE_NAME"; then
        print_error "Invalid service name: $SERVICE_NAME"
        show_help
        exit 1
    fi
    
    # Show status only
    if [ "$STATUS_ONLY" = true ]; then
        show_service_status "$SERVICE_NAME"
        exit 0
    fi
    
    # Restart service
    restart_service "$SERVICE_NAME"
    
    # Run migrations
    if [ "$NO_MIGRATIONS" = false ]; then
        run_migrations "$SERVICE_NAME"
    fi
    
    # Show status
    show_service_status "$SERVICE_NAME"
    
    # Show service info
    show_service_info "$SERVICE_NAME"
    
    print_success "Service $SERVICE_NAME restarted successfully!"
}

# Run main function
main "$@"
