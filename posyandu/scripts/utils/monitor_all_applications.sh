#!/bin/bash

# =============================================================================
# Monitor All Applications (Posyandu + dan POS BINDU PTM)
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

# Function to get service status
get_service_status() {
    local service_name="$1"
    local status=$(docker-compose ps --services --filter "status=running" | grep -q "$service_name" && echo "Running" || echo "Stopped")
    echo "$status"
}

# Function to get service health
get_service_health() {
    local service_name="$1"
    local port="$2"
    
    if [ -z "$port" ]; then
        echo "N/A"
        return
    fi
    
    if [ "$service_name" = "shared-database" ]; then
        # For database, check if container is running
        if docker-compose ps | grep -q "$service_name.*Up"; then
            echo "Healthy"
        else
            echo "Unhealthy"
        fi
    else
        # For other services, try to check HTTP endpoint
        if curl -s -f http://localhost:$port/ >/dev/null 2>&1; then
            echo "Healthy"
        else
            echo "Unhealthy"
        fi
    fi
}

# Function to get service resource usage
get_service_resources() {
    local service_name="$1"
    
    # Get container stats
    local stats=$(docker stats --no-stream --format "table {{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" "$service_name" 2>/dev/null | tail -n +2)
    
    if [ -n "$stats" ]; then
        echo "$stats"
    else
        echo "N/A"
    fi
}

# Function to show Posyandu + service status
show_posyandu_status() {
    print_title "Posyandu + Services Status"
    echo ""
    
    local services=(
        "shared-database:5432"
        "auth-service:8001"
        "posyandu-service:8002"
        "balita-service:8003"
        "ibu-hamil-service:8004"
        "imunisasi-service:8005"
        "kb-service:8006"
        "vitamin-service:8007"
        "rujukan-service:8008"
        "laporan-service:8009"
        "api-gateway:80"
        "frontend:3000"
    )
    
    printf "%-20s %-10s %-10s %-15s %-20s\n" "Service" "Status" "Health" "Port" "Resources"
    printf "%-20s %-10s %-10s %-15s %-20s\n" "-------" "------" "------" "----" "---------"
    
    for service_port in "${services[@]}"; do
        local service=$(echo $service_port | cut -d: -f1)
        local port=$(echo $service_port | cut -d: -f2)
        local status=$(get_service_status "$service")
        local health=$(get_service_health "$service" "$port")
        local resources=$(get_service_resources "$service" | awk '{print $1 " " $2}')
        
        # Color code status
        if [ "$status" = "Running" ]; then
            status="${GREEN}Running${NC}"
        else
            status="${RED}Stopped${NC}"
        fi
        
        # Color code health
        if [ "$health" = "Healthy" ]; then
            health="${GREEN}Healthy${NC}"
        elif [ "$health" = "Unhealthy" ]; then
            health="${RED}Unhealthy${NC}"
        else
            health="${YELLOW}N/A${NC}"
        fi
        
        printf "%-20s %-10s %-10s %-15s %-20s\n" "$service" "$status" "$health" "$port" "$resources"
    done
    echo ""
}

# Function to show POS BINDU service status
show_posbindu_status() {
    print_title "POS BINDU PTM Services Status"
    echo ""
    
    if [ ! -d "posbindu" ]; then
        print_warning "POS BINDU directory not found"
        return
    fi
    
    local services=(
        "shared-database:5433"
        "participant-service:8005"
        "screening-service:8006"
        "examination-service:8007"
        "lab-service:8008"
        "risk-assessment-service:8009"
        "intervention-service:8010"
        "referral-service:8011"
        "reporting-service:8012"
        "api-gateway:8080"
        "frontend:3001"
    )
    
    printf "%-20s %-10s %-10s %-15s %-20s\n" "Service" "Status" "Health" "Port" "Resources"
    printf "%-20s %-10s %-10s %-15s %-20s\n" "-------" "------" "------" "----" "---------"
    
    cd posbindu
    
    for service_port in "${services[@]}"; do
        local service=$(echo $service_port | cut -d: -f1)
        local port=$(echo $service_port | cut -d: -f2)
        local status=$(docker-compose ps --services --filter "status=running" | grep -q "$service" && echo "Running" || echo "Stopped")
        local health=$(get_service_health "$service" "$port")
        local resources=$(get_service_resources "$service" | awk '{print $1 " " $2}')
        
        # Color code status
        if [ "$status" = "Running" ]; then
            status="${GREEN}Running${NC}"
        else
            status="${RED}Stopped${NC}"
        fi
        
        # Color code health
        if [ "$health" = "Healthy" ]; then
            health="${GREEN}Healthy${NC}"
        elif [ "$health" = "Unhealthy" ]; then
            health="${RED}Unhealthy${NC}"
        else
            health="${YELLOW}N/A${NC}"
        fi
        
        printf "%-20s %-10s %-10s %-15s %-20s\n" "$service" "$status" "$health" "$port" "$resources"
    done
    
    cd ..
    echo ""
}

# Function to show combined service status
show_combined_status() {
    print_header "Combined Service Status Overview"
    echo ""
    
    show_posyandu_status
    show_posbindu_status
}

# Function to monitor services in real-time
monitor_real_time() {
    print_header "Real-time Service Monitoring"
    print_status "Press Ctrl+C to stop monitoring"
    echo ""
    
    while true; do
        clear
        show_combined_status
        echo "Last updated: $(date)"
        echo "Press Ctrl+C to stop monitoring"
        sleep 5
    done
}

# Function to check all endpoints
check_all_endpoints() {
    print_header "Endpoint Health Check"
    echo ""
    
    # Check Posyandu + endpoints
    print_title "Posyandu + Endpoints:"
    local posyandu_endpoints=(
        "http://localhost:8001/api/auth/"
        "http://localhost:8002/api/posyandu/"
        "http://localhost:8003/api/balita/"
        "http://localhost:8004/api/ibu-hamil/"
        "http://localhost:8005/api/imunisasi/"
        "http://localhost:8006/api/kb/"
        "http://localhost:8007/api/vitamin/"
        "http://localhost:8008/api/rujukan/"
        "http://localhost:8009/api/laporan/"
        "http://localhost/"
        "http://localhost:3000/"
    )
    
    for endpoint in "${posyandu_endpoints[@]}"; do
        local service_name=$(echo "$endpoint" | sed 's|http://localhost:||' | sed 's|/api/.*||' | sed 's|/||')
        print_status "Checking $service_name: $endpoint"
        
        if curl -s -f "$endpoint" >/dev/null 2>&1; then
            print_success "$service_name is accessible"
        else
            print_error "$service_name is not accessible"
        fi
    done
    
    # Check POS BINDU endpoints
    if [ -d "posbindu" ]; then
        print_title "POS BINDU PTM Endpoints:"
        local posbindu_endpoints=(
            "http://localhost:8005/api/participant/"
            "http://localhost:8006/api/screening/"
            "http://localhost:8007/api/examination/"
            "http://localhost:8008/api/lab/"
            "http://localhost:8009/api/risk-assessment/"
            "http://localhost:8010/api/intervention/"
            "http://localhost:8011/api/referral/"
            "http://localhost:8012/api/reporting/"
            "http://localhost:8080/"
            "http://localhost:3001/"
        )
        
        for endpoint in "${posbindu_endpoints[@]}"; do
            local service_name=$(echo "$endpoint" | sed 's|http://localhost:||' | sed 's|/api/.*||' | sed 's|/||')
            print_status "Checking $service_name: $endpoint"
            
            if curl -s -f "$endpoint" >/dev/null 2>&1; then
                print_success "$service_name is accessible"
            else
                print_error "$service_name is not accessible"
            fi
        done
    fi
    echo ""
}

# Function to show system resources
show_system_resources() {
    print_header "System Resource Usage"
    echo ""
    
    # Docker system info
    print_status "Docker System Information:"
    docker system df
    echo ""
    
    # Container resource usage
    print_status "Container Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"
    echo ""
}

# Function to show detailed service information
show_detailed_service_info() {
    local service_name="$1"
    
    if [ -z "$service_name" ]; then
        print_error "Service name is required"
        return 1
    fi
    
    print_header "Detailed Information for $service_name"
    echo ""
    
    # Check if service is in Posyandu + or POS BINDU
    local is_posyandu=false
    local is_posbindu=false
    
    if docker-compose ps | grep -q "$service_name"; then
        is_posyandu=true
    elif [ -d "posbindu" ] && cd posbindu && docker-compose ps | grep -q "$service_name"; then
        is_posbindu=true
        cd ..
    fi
    
    if [ "$is_posyandu" = true ]; then
        print_status "Service found in Posyandu +"
        docker-compose ps "$service_name"
        echo ""
        docker-compose logs --tail=10 "$service_name"
    elif [ "$is_posbindu" = true ]; then
        print_status "Service found in POS BINDU PTM"
        cd posbindu
        docker-compose ps "$service_name"
        echo ""
        docker-compose logs --tail=10 "$service_name"
        cd ..
    else
        print_error "Service $service_name not found in any application"
        return 1
    fi
    echo ""
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS] [SERVICE_NAME]"
    echo ""
    echo "Options:"
    echo "  --status           Show combined service status overview"
    echo "  --posyandu         Show only Posyandu + service status"
    echo "  --posbindu         Show only POS BINDU PTM service status"
    echo "  --monitor          Monitor services in real-time"
    echo "  --endpoints        Check all endpoints"
    echo "  --resources        Show system resource usage"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --status        Show status overview"
    echo "  $0 --monitor       Monitor in real-time"
    echo "  $0 --endpoints     Check all endpoints"
    echo "  $0 auth-service    Show detailed info for auth-service"
    echo "  $0 --resources     Show system resources"
}

# Main execution
main() {
    echo "============================================================================="
    echo "📊 Monitor All Applications (Posyandu + & POS BINDU PTM)"
    echo "============================================================================="
    echo ""
    
    # Check prerequisites
    check_docker
    
    # Parse command line arguments
    SHOW_STATUS=false
    SHOW_POSYANDU=false
    SHOW_POSBINDU=false
    MONITOR_REAL_TIME=false
    CHECK_ENDPOINTS=false
    SHOW_RESOURCES=false
    SERVICE_NAME=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --status)
                SHOW_STATUS=true
                shift
                ;;
            --posyandu)
                SHOW_POSYANDU=true
                shift
                ;;
            --posbindu)
                SHOW_POSBINDU=true
                shift
                ;;
            --monitor)
                MONITOR_REAL_TIME=true
                shift
                ;;
            --endpoints)
                CHECK_ENDPOINTS=true
                shift
                ;;
            --resources)
                SHOW_RESOURCES=true
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
    
    # Execute based on options
    if [ "$MONITOR_REAL_TIME" = true ]; then
        monitor_real_time
    elif [ "$SHOW_STATUS" = true ]; then
        show_combined_status
    elif [ "$SHOW_POSYANDU" = true ]; then
        show_posyandu_status
    elif [ "$SHOW_POSBINDU" = true ]; then
        show_posbindu_status
    elif [ "$CHECK_ENDPOINTS" = true ]; then
        check_all_endpoints
    elif [ "$SHOW_RESOURCES" = true ]; then
        show_system_resources
    elif [ -n "$SERVICE_NAME" ]; then
        show_detailed_service_info "$SERVICE_NAME"
    else
        # Default: show combined status overview
        show_combined_status
    fi
}

# Run main function
main "$@"