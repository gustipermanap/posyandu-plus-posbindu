#!/bin/bash

# =============================================================================
# Script: Test Posyandu+ API Endpoints
# Description: Test API endpoints untuk Posyandu+ services
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
    echo "  --all             Test all services"
    echo "  --health          Test health endpoints only"
    echo "  --auth            Test authentication endpoints"
    echo "  --verbose         Verbose output"
    echo "  --help            Show this help message"
    echo ""
    echo "Arguments:"
    echo "  SERVICE_NAME      Test specific service"
    echo ""
    echo "Examples:"
    echo "  $0                # Test all services"
    echo "  $0 --all          # Test all services"
    echo "  $0 auth-service   # Test specific service"
    echo "  $0 --health       # Test health endpoints only"
}

# Function untuk test endpoint
test_endpoint() {
    local url="$1"
    local method="${2:-GET}"
    local expected_status="${3:-200}"
    local description="$4"
    
    if [ -n "$description" ]; then
        echo -n "Testing $description... "
    else
        echo -n "Testing $method $url... "
    fi
    
    # Make request
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "%{http_code}" -o /dev/null "$url" 2>/dev/null || echo "000")
    else
        response=$(curl -s -w "%{http_code}" -o /dev/null -X "$method" "$url" 2>/dev/null || echo "000")
    fi
    
    # Check response
    if [ "$response" = "$expected_status" ]; then
        print_success "OK ($response)"
        return 0
    else
        print_error "FAILED ($response)"
        return 1
    fi
}

# Function untuk test service
test_service() {
    local service_name="$1"
    local port="$2"
    local base_url="http://localhost:$port"
    
    print_header "Testing $service_name (Port $port)"
    
    local passed=0
    local total=0
    
    # Health check
    total=$((total + 1))
    if test_endpoint "$base_url/health" "GET" "200" "Health check"; then
        passed=$((passed + 1))
    fi
    
    # API endpoints based on service
    case $service_name in
        "auth-service")
            total=$((total + 1))
            if test_endpoint "$base_url/api/auth/login/" "POST" "405" "Login endpoint"; then
                passed=$((passed + 1))
            fi
            
            total=$((total + 1))
            if test_endpoint "$base_url/api/auth/register/" "POST" "405" "Register endpoint"; then
                passed=$((passed + 1))
            fi
            ;;
            
        "posyandu-service")
            total=$((total + 1))
            if test_endpoint "$base_url/api/posyandu/" "GET" "401" "Posyandu list"; then
                passed=$((passed + 1))
            fi
            ;;
            
        "balita-service")
            total=$((total + 1))
            if test_endpoint "$base_url/api/balita/" "GET" "401" "Balita list"; then
                passed=$((passed + 1))
            fi
            ;;
            
        "ibu-hamil-service")
            total=$((total + 1))
            if test_endpoint "$base_url/api/ibu-hamil/" "GET" "401" "Ibu hamil list"; then
                passed=$((passed + 1))
            fi
            ;;
            
        "imunisasi-service")
            total=$((total + 1))
            if test_endpoint "$base_url/api/imunisasi/" "GET" "401" "Imunisasi list"; then
                passed=$((passed + 1))
            fi
            ;;
            
        "kb-service")
            total=$((total + 1))
            if test_endpoint "$base_url/api/kb/" "GET" "401" "KB list"; then
                passed=$((passed + 1))
            fi
            ;;
            
        "vitamin-service")
            total=$((total + 1))
            if test_endpoint "$base_url/api/vitamin/" "GET" "401" "Vitamin list"; then
                passed=$((passed + 1))
            fi
            ;;
            
        "rujukan-service")
            total=$((total + 1))
            if test_endpoint "$base_url/api/rujukan/" "GET" "401" "Rujukan list"; then
                passed=$((passed + 1))
            fi
            ;;
            
        "laporan-service")
            total=$((total + 1))
            if test_endpoint "$base_url/api/laporan/" "GET" "401" "Laporan list"; then
                passed=$((passed + 1))
            fi
            ;;
    esac
    
    # Summary
    echo ""
    if [ $passed -eq $total ]; then
        print_success "$service_name: $passed/$total tests passed"
    else
        print_warning "$service_name: $passed/$total tests passed"
    fi
    
    return $((total - passed))
}

# Function untuk test health endpoints only
test_health_endpoints() {
    print_header "Health Endpoints Test"
    
    local services=(
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
    
    local passed=0
    local total=${#services[@]}
    
    for service_port in "${services[@]}"; do
        service=$(echo $service_port | cut -d: -f1)
        port=$(echo $service_port | cut -d: -f2)
        
        if test_endpoint "http://localhost:$port/health" "GET" "200" "$service health"; then
            passed=$((passed + 1))
        fi
    done
    
    echo ""
    if [ $passed -eq $total ]; then
        print_success "Health check: $passed/$total services healthy"
    else
        print_warning "Health check: $passed/$total services healthy"
    fi
    
    return $((total - passed))
}

# Function untuk test authentication
test_authentication() {
    print_header "Authentication Test"
    
    local auth_url="http://localhost:8001"
    local passed=0
    local total=0
    
    # Test login endpoint
    total=$((total + 1))
    if test_endpoint "$auth_url/api/auth/login/" "POST" "405" "Login endpoint"; then
        passed=$((passed + 1))
    fi
    
    # Test register endpoint
    total=$((total + 1))
    if test_endpoint "$auth_url/api/auth/register/" "POST" "405" "Register endpoint"; then
        passed=$((passed + 1))
    fi
    
    # Test token refresh
    total=$((total + 1))
    if test_endpoint "$auth_url/api/auth/token/refresh/" "POST" "405" "Token refresh"; then
        passed=$((passed + 1))
    fi
    
    echo ""
    if [ $passed -eq $total ]; then
        print_success "Authentication: $passed/$total tests passed"
    else
        print_warning "Authentication: $passed/$total tests passed"
    fi
    
    return $((total - passed))
}

# Function untuk test all services
test_all_services() {
    print_header "Testing All Posyandu+ Services"
    
    local services=(
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
    
    local total_failed=0
    
    for service_port in "${services[@]}"; do
        service=$(echo $service_port | cut -d: -f1)
        port=$(echo $service_port | cut -d: -f2)
        
        test_service "$service" "$port"
        total_failed=$((total_failed + $?))
        
        echo ""
    done
    
    # Test frontend
    print_header "Testing Frontend"
    if test_endpoint "http://localhost:3000" "GET" "200" "Frontend"; then
        print_success "Frontend is accessible"
    else
        print_error "Frontend is not accessible"
        total_failed=$((total_failed + 1))
    fi
    
    # Test API Gateway
    print_header "Testing API Gateway"
    if test_endpoint "http://localhost" "GET" "200" "API Gateway"; then
        print_success "API Gateway is accessible"
    else
        print_error "API Gateway is not accessible"
        total_failed=$((total_failed + 1))
    fi
    
    # Summary
    echo ""
    print_header "Test Summary"
    if [ $total_failed -eq 0 ]; then
        print_success "All tests passed!"
    else
        print_warning "$total_failed tests failed"
    fi
    
    return $total_failed
}

# Parse arguments
MODE="all"
SERVICE_NAME=""
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            MODE="all"
            shift
            ;;
        --health)
            MODE="health"
            shift
            ;;
        --auth)
            MODE="auth"
            shift
            ;;
        --verbose)
            VERBOSE=true
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

# Check if curl is available
if ! command -v curl &> /dev/null; then
    print_error "curl is not installed. Please install curl first."
    exit 1
fi

# Execute based on mode
case $MODE in
    "all")
        if [ -n "$SERVICE_NAME" ]; then
            # Test specific service
            case $SERVICE_NAME in
                "auth-service")
                    test_service "auth-service" "8001"
                    ;;
                "posyandu-service")
                    test_service "posyandu-service" "8002"
                    ;;
                "balita-service")
                    test_service "balita-service" "8003"
                    ;;
                "ibu-hamil-service")
                    test_service "ibu-hamil-service" "8004"
                    ;;
                "imunisasi-service")
                    test_service "imunisasi-service" "8005"
                    ;;
                "kb-service")
                    test_service "kb-service" "8006"
                    ;;
                "vitamin-service")
                    test_service "vitamin-service" "8007"
                    ;;
                "rujukan-service")
                    test_service "rujukan-service" "8008"
                    ;;
                "laporan-service")
                    test_service "laporan-service" "8009"
                    ;;
                *)
                    print_error "Unknown service: $SERVICE_NAME"
                    exit 1
                    ;;
            esac
        else
            test_all_services
        fi
        ;;
    "health")
        test_health_endpoints
        ;;
    "auth")
        test_authentication
        ;;
    *)
        test_all_services
        ;;
esac
