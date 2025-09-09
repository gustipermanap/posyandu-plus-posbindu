#!/bin/bash

# =============================================================================
# Script: Stop All Posyandu+ Services
# Description: Stop semua Posyandu+ microservices menggunakan Docker Compose
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
    echo "Usage: $0 [OPTIONS] [SERVICE_NAME]"
    echo ""
    echo "Options:"
    echo "  --cleanup         Remove containers and volumes"
    echo "  --help            Show this help message"
    echo ""
    echo "Arguments:"
    echo "  SERVICE_NAME      Stop specific service only"
    echo ""
    echo "Examples:"
    echo "  $0                 # Stop semua services"
    echo "  $0 --cleanup       # Stop dan cleanup containers"
    echo "  $0 auth-service    # Stop specific service"
}

# Parse arguments
CLEANUP=false
SERVICE_NAME=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --cleanup)
            CLEANUP=true
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
                print_error "Multiple service names provided. Please specify only one."
                exit 1
            fi
            shift
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

# Stop specific service or all services
if [ -n "$SERVICE_NAME" ]; then
    print_status "Stopping service: $SERVICE_NAME"
    
    if docker-compose ps | grep -q "$SERVICE_NAME"; then
        docker-compose stop "$SERVICE_NAME"
        print_success "Service $SERVICE_NAME stopped successfully"
        
        if [ "$CLEANUP" = true ]; then
            print_status "Removing container for $SERVICE_NAME..."
            docker-compose rm -f "$SERVICE_NAME"
            print_success "Container for $SERVICE_NAME removed"
        fi
    else
        print_warning "Service $SERVICE_NAME is not running"
    fi
else
    print_status "Stopping all Posyandu+ services..."
    
    # Stop all services
    docker-compose stop
    
    print_success "All services stopped successfully"
    
    # Cleanup if requested
    if [ "$CLEANUP" = true ]; then
        print_status "Cleaning up containers and volumes..."
        
        # Remove containers
        docker-compose rm -f
        
        # Remove volumes (optional - be careful with this)
        read -p "Do you want to remove volumes as well? This will delete all data! (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v
            print_warning "All volumes removed. Data has been deleted!"
        else
            print_status "Volumes preserved"
        fi
        
        print_success "Cleanup completed"
    fi
fi

# Show remaining containers
echo ""
print_status "Remaining containers:"
docker-compose ps

echo ""
print_success "Stop operation completed!"
