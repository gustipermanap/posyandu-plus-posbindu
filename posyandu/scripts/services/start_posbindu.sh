#!/bin/bash

# =============================================================================
# Start POS BINDU PTM Microservices
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

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to check if POS BINDU directory exists
check_posbindu_directory() {
    if [ ! -d "posbindu" ]; then
        print_error "POS BINDU directory not found. Please ensure you're in the correct project directory."
        exit 1
    fi
}

# Function to start POS BINDU services
start_posbindu_services() {
    print_header "Starting POS BINDU PTM Microservices..."
    
    # Change to POS BINDU directory
    cd posbindu
    
    # Check if docker-compose.yml exists
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found in posbindu directory"
        exit 1
    fi
    
    # Start services
    print_status "Starting POS BINDU services..."
    docker-compose up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 20
    
    # Run migrations
    print_status "Running database migrations..."
    
    services=(
        "participant-service"
        "screening-service"
        "examination-service"
        "lab-service"
        "risk-assessment-service"
        "intervention-service"
        "referral-service"
        "reporting-service"
    )
    
    for service in "${services[@]}"; do
        print_status "Running migrations for $service..."
        docker-compose exec -T "$service" python manage.py makemigrations || true
        docker-compose exec -T "$service" python manage.py migrate || true
    done
    
    # Create superuser
    print_status "Creating superuser..."
    docker-compose exec -T participant-service python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@posbindu.com', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF
    
    print_success "POS BINDU services started successfully"
    
    # Return to project root
    cd ..
}

# Function to show service status
show_service_status() {
    print_header "POS BINDU Service Status:"
    echo ""
    
    cd posbindu
    docker-compose ps
    cd ..
    echo ""
}

# Function to show access information
show_access_info() {
    echo ""
    echo "============================================================================="
    echo "🚀 POS BINDU PTM Services Started Successfully!"
    echo "============================================================================="
    echo ""
    echo "🌐 Access URLs:"
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
    echo "🔑 Login Credentials:"
    echo "  - Username: admin"
    echo "  - Password: admin123"
    echo ""
    echo "📊 Useful Commands:"
    echo "  - View logs: cd posbindu && docker-compose logs -f [service-name]"
    echo "  - Stop all: cd posbindu && docker-compose down"
    echo "  - Restart service: cd posbindu && docker-compose restart [service-name]"
    echo "  - Shell access: cd posbindu && docker-compose exec [service-name] bash"
    echo ""
    echo "============================================================================="
}

# Function to stop POS BINDU services
stop_posbindu_services() {
    print_header "Stopping POS BINDU PTM Services..."
    
    cd posbindu
    docker-compose down
    cd ..
    
    print_success "POS BINDU services stopped successfully"
}

# Function to restart POS BINDU services
restart_posbindu_services() {
    print_header "Restarting POS BINDU PTM Services..."
    
    stop_posbindu_services
    start_posbindu_services
    show_access_info
    
    print_success "POS BINDU services restarted successfully"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --start            Start POS BINDU services"
    echo "  --stop             Stop POS BINDU services"
    echo "  --restart          Restart POS BINDU services"
    echo "  --status           Show service status"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --start         Start POS BINDU services"
    echo "  $0 --stop          Stop POS BINDU services"
    echo "  $0 --status        Show service status"
}

# Main execution
main() {
    echo "============================================================================="
    echo "🏥 Starting POS BINDU PTM Microservices"
    echo "============================================================================="
    echo ""
    
    # Check prerequisites
    check_docker
    check_posbindu_directory
    
    # Parse command line arguments
    START=false
    STOP=false
    RESTART=false
    STATUS=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --start)
                START=true
                shift
                ;;
            --stop)
                STOP=true
                shift
                ;;
            --restart)
                RESTART=true
                shift
                ;;
            --status)
                STATUS=true
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
                print_error "Unknown argument: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Execute based on options
    if [ "$STOP" = true ]; then
        stop_posbindu_services
    elif [ "$RESTART" = true ]; then
        restart_posbindu_services
    elif [ "$STATUS" = true ]; then
        show_service_status
    elif [ "$START" = true ]; then
        start_posbindu_services
        show_service_status
        show_access_info
        print_success "POS BINDU services started successfully!"
    else
        # Default: start services
        start_posbindu_services
        show_service_status
        show_access_info
        print_success "POS BINDU services started successfully!"
    fi
}

# Run main function
main "$@"
