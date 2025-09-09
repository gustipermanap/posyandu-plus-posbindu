#!/bin/bash

# =============================================================================
# Stop All Applications (Posyandu + dan POS BINDU PTM)
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

# Function to stop all applications
stop_all_applications() {
    print_header "Stopping All Applications..."
    
    # Stop Posyandu + services
    print_status "Stopping Posyandu + services..."
    if docker-compose ps | grep -q "Up"; then
        docker-compose down
        print_success "Posyandu + services stopped"
    else
        print_warning "Posyandu + services are not running"
    fi
    
    # Stop POS BINDU services
    print_status "Stopping POS BINDU PTM services..."
    if [ -d "posbindu" ]; then
        cd posbindu
        if docker-compose ps | grep -q "Up"; then
            docker-compose down
            print_success "POS BINDU PTM services stopped"
        else
            print_warning "POS BINDU PTM services are not running"
        fi
        cd ..
    else
        print_warning "POS BINDU directory not found"
    fi
    
    print_success "All applications stopped successfully"
}

# Function to stop with cleanup
stop_with_cleanup() {
    print_header "Stopping All Applications with Cleanup..."
    
    # Stop Posyandu + services with cleanup
    print_status "Stopping Posyandu + services with cleanup..."
    if docker-compose ps | grep -q "Up"; then
        docker-compose down -v --remove-orphans
        print_success "Posyandu + services stopped and cleaned up"
    else
        print_warning "Posyandu + services are not running"
    fi
    
    # Stop POS BINDU services with cleanup
    print_status "Stopping POS BINDU PTM services with cleanup..."
    if [ -d "posbindu" ]; then
        cd posbindu
        if docker-compose ps | grep -q "Up"; then
            docker-compose down -v --remove-orphans
            print_success "POS BINDU PTM services stopped and cleaned up"
        else
            print_warning "POS BINDU PTM services are not running"
        fi
        cd ..
    else
        print_warning "POS BINDU directory not found"
    fi
    
    # Clean up unused Docker resources
    print_status "Cleaning up unused Docker resources..."
    docker container prune -f
    docker image prune -f
    docker volume prune -f
    docker network prune -f
    
    print_success "All applications stopped and cleaned up successfully"
}

# Function to show service status
show_service_status() {
    print_header "Service Status:"
    echo ""
    
    print_status "Posyandu + Services:"
    docker-compose ps
    echo ""
    
    if [ -d "posbindu" ]; then
        print_status "POS BINDU PTM Services:"
        cd posbindu
        docker-compose ps
        cd ..
    else
        print_warning "POS BINDU directory not found"
    fi
    echo ""
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --stop             Stop all applications"
    echo "  --cleanup          Stop all applications with cleanup"
    echo "  --status           Show service status"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --stop          Stop all applications"
    echo "  $0 --cleanup       Stop all applications with cleanup"
    echo "  $0 --status        Show service status"
}

# Main execution
main() {
    echo "============================================================================="
    echo "🛑 Stopping All Applications (Posyandu + & POS BINDU PTM)"
    echo "============================================================================="
    echo ""
    
    # Check prerequisites
    check_docker
    
    # Parse command line arguments
    STOP=false
    CLEANUP=false
    STATUS=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --stop)
                STOP=true
                shift
                ;;
            --cleanup)
                CLEANUP=true
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
    if [ "$STATUS" = true ]; then
        show_service_status
    elif [ "$CLEANUP" = true ]; then
        stop_with_cleanup
    elif [ "$STOP" = true ]; then
        stop_all_applications
    else
        # Default: stop all applications
        stop_all_applications
    fi
}

# Run main function
main "$@"
