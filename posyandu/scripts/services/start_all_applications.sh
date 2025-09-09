#!/bin/bash

# =============================================================================
# Start All Applications (Posyandu + dan POS BINDU PTM)
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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

print_title() {
    echo -e "${CYAN}[TITLE]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to start Posyandu + services
start_posyandu_services() {
    print_title "Starting Posyandu + Microservices..."
    
    # Start Posyandu + services
    "$(dirname "$0")/start_all_services.sh"
    
    print_success "Posyandu + services started"
}

# Function to start POS BINDU PTM services
start_posbindu_services() {
    print_title "Starting POS BINDU PTM Microservices..."
    
    # Start POS BINDU services
    "$(dirname "$0")/start_posbindu.sh" --start
    
    print_success "POS BINDU PTM services started"
}

# Function to show combined service status
show_combined_status() {
    print_header "Combined Service Status"
    echo ""
    
    print_title "Posyandu + Services:"
    docker-compose ps
    echo ""
    
    print_title "POS BINDU PTM Services:"
    cd posbindu
    docker-compose ps
    cd ..
    echo ""
}

# Function to show combined access information
show_combined_access_info() {
    echo ""
    echo "============================================================================="
    echo "🚀 All Applications Started Successfully!"
    echo "============================================================================="
    echo ""
    echo "📱 POSYANDU + APPLICATION:"
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
    echo "🏥 POS BINDU PTM APPLICATION:"
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
    echo "🔑 LOGIN CREDENTIALS:"
    echo "  - Username: admin"
    echo "  - Password: admin123"
    echo ""
    echo "📊 USEFUL COMMANDS:"
    echo "  - Stop Posyandu +: docker-compose down"
    echo "  - Stop POS BINDU: cd posbindu && docker-compose down"
    echo "  - Stop all: ./scripts/services/stop_all_applications.sh"
    echo "  - View logs: docker-compose logs -f [service-name]"
    echo "  - Monitor: ./scripts/utils/monitor_services.sh --monitor"
    echo ""
    echo "============================================================================="
}

# Function to stop all applications
stop_all_applications() {
    print_header "Stopping All Applications..."
    
    # Stop Posyandu + services
    print_status "Stopping Posyandu + services..."
    docker-compose down
    
    # Stop POS BINDU services
    print_status "Stopping POS BINDU PTM services..."
    cd posbindu
    docker-compose down
    cd ..
    
    print_success "All applications stopped successfully"
}

# Function to restart all applications
restart_all_applications() {
    print_header "Restarting All Applications..."
    
    stop_all_applications
    start_posyandu_services
    start_posbindu_services
    show_combined_access_info
    
    print_success "All applications restarted successfully"
}

# Function to test all endpoints
test_all_endpoints() {
    print_header "Testing All Application Endpoints..."
    
    # Test Posyandu + endpoints
    print_title "Testing Posyandu + Endpoints:"
    "$(dirname "$0")/../utils/test_api.sh" --all
    
    # Test POS BINDU endpoints
    print_title "Testing POS BINDU PTM Endpoints:"
    cd posbindu
    # Note: You would need to create a similar test script for POS BINDU
    # For now, just test basic connectivity
    print_status "Testing POS BINDU endpoints..."
    curl -s http://localhost:3001/ >/dev/null && print_success "POS BINDU Frontend is accessible" || print_warning "POS BINDU Frontend is not accessible"
    curl -s http://localhost:8080/ >/dev/null && print_success "POS BINDU API Gateway is accessible" || print_warning "POS BINDU API Gateway is not accessible"
    cd ..
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --start            Start all applications"
    echo "  --stop             Stop all applications"
    echo "  --restart          Restart all applications"
    echo "  --status           Show combined service status"
    echo "  --test             Test all endpoints"
    echo "  --posyandu-only    Start only Posyandu + services"
    echo "  --posbindu-only    Start only POS BINDU PTM services"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --start         Start all applications"
    echo "  $0 --stop          Stop all applications"
    echo "  $0 --status        Show service status"
    echo "  $0 --test          Test all endpoints"
}

# Main execution
main() {
    echo "============================================================================="
    echo "🚀 Starting All Applications (Posyandu + & POS BINDU PTM)"
    echo "============================================================================="
    echo ""
    
    # Check prerequisites
    check_docker
    
    # Parse command line arguments
    START=false
    STOP=false
    RESTART=false
    STATUS=false
    TEST=false
    POSYANDU_ONLY=false
    POSBINDU_ONLY=false
    
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
            --test)
                TEST=true
                shift
                ;;
            --posyandu-only)
                POSYANDU_ONLY=true
                shift
                ;;
            --posbindu-only)
                POSBINDU_ONLY=true
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
        stop_all_applications
    elif [ "$RESTART" = true ]; then
        restart_all_applications
    elif [ "$STATUS" = true ]; then
        show_combined_status
    elif [ "$TEST" = true ]; then
        test_all_endpoints
    elif [ "$POSYANDU_ONLY" = true ]; then
        start_posyandu_services
        print_success "Posyandu + services started successfully!"
    elif [ "$POSBINDU_ONLY" = true ]; then
        start_posbindu_services
        print_success "POS BINDU PTM services started successfully!"
    elif [ "$START" = true ]; then
        start_posyandu_services
        start_posbindu_services
        show_combined_status
        show_combined_access_info
        print_success "All applications started successfully!"
    else
        # Default: start all applications
        start_posyandu_services
        start_posbindu_services
        show_combined_status
        show_combined_access_info
        print_success "All applications started successfully!"
    fi
}

# Run main function
main "$@"
