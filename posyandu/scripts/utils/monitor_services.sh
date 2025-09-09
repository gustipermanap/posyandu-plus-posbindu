#!/bin/bash

# =============================================================================
# Script: Monitor Posyandu+ Services
# Description: Monitor status, logs, dan health check untuk Posyandu+ services
# Author: Posyandu+ Development Team
# Version: 1.0
# =============================================================================

set -e

# Colors untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

print_header() {
    echo -e "${CYAN}=== $1 ===${NC}"
}

# Function untuk menampilkan help
show_help() {
    echo "Usage: $0 [OPTIONS] [SERVICE_NAME]"
    echo ""
    echo "Options:"
    echo "  --status          Show service status overview"
    echo "  --monitor         Real-time monitoring"
    echo "  --endpoints       Health check endpoints"
    echo "  --resources       System resources usage"
    echo "  --logs            Show logs for all services"
    echo "  --help            Show this help message"
    echo ""
    echo "Arguments:"
    echo "  SERVICE_NAME      Monitor specific service"
    echo ""
    echo "Examples:"
    echo "  $0 --status       # Show status overview"
    echo "  $0 --monitor      # Real-time monitoring"
    echo "  $0 auth-service   # Monitor specific service"
}

# Function untuk check service status
check_status() {
    print_header "Service Status Overview"
    
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found. Please run from project root."
        exit 1
    fi
    
    echo "Container Status:"
    docker-compose ps
    
    echo ""
    echo "Service Health:"
    
    # List of services to check
    services=(
        "auth-service:8001"
        "posyandu-service:8002"
        "balita-service:8003"
        "ibu-hamil-service:8004"
        "imunisasi-service:8005"
        "kb-service:8006"
        "vitamin-service:8007"
        "rujukan-service:8008"
        "laporan-service:8009"
        "frontend:3000"
    )
    
    for service_port in "${services[@]}"; do
        service=$(echo $service_port | cut -d: -f1)
        port=$(echo $service_port | cut -d: -f2)
        
        if curl -s -f "http://localhost:$port/health" > /dev/null 2>&1; then
            print_success "$service (port $port): Healthy"
        else
            print_warning "$service (port $port): Unhealthy or not responding"
        fi
    done
}

# Function untuk real-time monitoring
real_time_monitor() {
    print_header "Real-time Monitoring"
    print_status "Press Ctrl+C to stop monitoring"
    
    while true; do
        clear
        print_header "Posyandu+ Services Monitor - $(date)"
        
        echo "Container Status:"
        docker-compose ps
        
        echo ""
        echo "Resource Usage:"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
        
        echo ""
        echo "Recent Logs (last 5 lines per service):"
        docker-compose logs --tail=5 --timestamps
        
        sleep 5
    done
}

# Function untuk health check endpoints
check_endpoints() {
    print_header "Health Check Endpoints"
    
    # List of services and their health endpoints
    services=(
        "auth-service:8001"
        "posyandu-service:8002"
        "balita-service:8003"
        "ibu-hamil-service:8004"
        "imunisasi-service:8005"
        "kb-service:8006"
        "vitamin-service:8007"
        "rujukan-service:8008"
        "laporan-service:8009"
    )
    
    for service_port in "${services[@]}"; do
        service=$(echo $service_port | cut -d: -f1)
        port=$(echo $service_port | cut -d: -f2)
        
        echo -n "Checking $service (port $port)... "
        
        if curl -s -f "http://localhost:$port/health" > /dev/null 2>&1; then
            print_success "OK"
        else
            print_error "FAILED"
        fi
    done
    
    # Check frontend
    echo -n "Checking frontend (port 3000)... "
    if curl -s -f "http://localhost:3000" > /dev/null 2>&1; then
        print_success "OK"
    else
        print_error "FAILED"
    fi
    
    # Check API Gateway
    echo -n "Checking API Gateway (port 80)... "
    if curl -s -f "http://localhost" > /dev/null 2>&1; then
        print_success "OK"
    else
        print_error "FAILED"
    fi
}

# Function untuk system resources
check_resources() {
    print_header "System Resources"
    
    echo "Docker System Info:"
    docker system df
    
    echo ""
    echo "Container Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"
    
    echo ""
    echo "Disk Usage:"
    df -h
    
    echo ""
    echo "Memory Usage:"
    free -h
}

# Function untuk show logs
show_logs() {
    print_header "Service Logs"
    
    if [ -n "$1" ]; then
        print_status "Showing logs for: $1"
        docker-compose logs -f "$1"
    else
        print_status "Showing logs for all services"
        docker-compose logs -f
    fi
}

# Function untuk monitor specific service
monitor_service() {
    local service_name="$1"
    
    print_header "Monitoring Service: $service_name"
    
    # Check if service exists
    if ! docker-compose ps | grep -q "$service_name"; then
        print_error "Service $service_name not found or not running"
        exit 1
    fi
    
    echo "Service Status:"
    docker-compose ps "$service_name"
    
    echo ""
    echo "Service Logs (last 20 lines):"
    docker-compose logs --tail=20 "$service_name"
    
    echo ""
    echo "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}" | grep "$service_name"
    
    echo ""
    echo "To follow logs in real-time:"
    echo "docker-compose logs -f $service_name"
}

# Parse arguments
MODE="status"
SERVICE_NAME=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --status)
            MODE="status"
            shift
            ;;
        --monitor)
            MODE="monitor"
            shift
            ;;
        --endpoints)
            MODE="endpoints"
            shift
            ;;
        --resources)
            MODE="resources"
            shift
            ;;
        --logs)
            MODE="logs"
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

# Execute based on mode
case $MODE in
    "status")
        check_status
        ;;
    "monitor")
        real_time_monitor
        ;;
    "endpoints")
        check_endpoints
        ;;
    "resources")
        check_resources
        ;;
    "logs")
        show_logs "$SERVICE_NAME"
        ;;
    *)
        if [ -n "$SERVICE_NAME" ]; then
            monitor_service "$SERVICE_NAME"
        else
            check_status
        fi
        ;;
esac
