#!/bin/bash

# =============================================================================
# Test All Applications (Posyandu + dan POS BINDU PTM)
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

# API endpoints for Posyandu +
declare -A POSYANDU_ENDPOINTS=(
    ["auth-service"]="http://localhost:8001/api/auth/"
    ["posyandu-service"]="http://localhost:8002/api/posyandu/"
    ["balita-service"]="http://localhost:8003/api/balita/"
    ["ibu-hamil-service"]="http://localhost:8004/api/ibu-hamil/"
    ["imunisasi-service"]="http://localhost:8005/api/imunisasi/"
    ["kb-service"]="http://localhost:8006/api/kb/"
    ["vitamin-service"]="http://localhost:8007/api/vitamin/"
    ["rujukan-service"]="http://localhost:8008/api/rujukan/"
    ["laporan-service"]="http://localhost:8009/api/laporan/"
    ["frontend"]="http://localhost:3000/"
)

# API endpoints for POS BINDU PTM
declare -A POSBINDU_ENDPOINTS=(
    ["participant-service"]="http://localhost:8005/api/participant/"
    ["screening-service"]="http://localhost:8006/api/screening/"
    ["examination-service"]="http://localhost:8007/api/examination/"
    ["lab-service"]="http://localhost:8008/api/lab/"
    ["risk-assessment-service"]="http://localhost:8009/api/risk-assessment/"
    ["intervention-service"]="http://localhost:8010/api/intervention/"
    ["referral-service"]="http://localhost:8011/api/referral/"
    ["reporting-service"]="http://localhost:8012/api/reporting/"
    ["frontend"]="http://localhost:3001/"
)

# Function to test endpoint
test_endpoint() {
    local service_name="$1"
    local endpoint="$2"
    local expected_status="${3:-200}"
    
    print_status "Testing $service_name: $endpoint"
    
    # Make HTTP request
    local response=$(curl -s -w "%{http_code}" -o /dev/null "$endpoint" 2>/dev/null || echo "000")
    
    if [ "$response" = "$expected_status" ]; then
        print_success "$service_name is accessible (HTTP $response)"
        return 0
    else
        print_error "$service_name is not accessible (HTTP $response)"
        return 1
    fi
}

# Function to test Posyandu + endpoints
test_posyandu_endpoints() {
    print_title "Testing Posyandu + Endpoints"
    
    local success_count=0
    local total_count=0
    
    for service in "${!POSYANDU_ENDPOINTS[@]}"; do
        local endpoint="${POSYANDU_ENDPOINTS[$service]}"
        total_count=$((total_count + 1))
        
        if test_endpoint "$service" "$endpoint"; then
            success_count=$((success_count + 1))
        fi
    done
    
    echo ""
    print_header "Posyandu + Test Results"
    echo "Successful: $success_count/$total_count"
    
    if [ $success_count -eq $total_count ]; then
        print_success "All Posyandu + endpoints are accessible!"
    else
        print_warning "Some Posyandu + endpoints are not accessible"
    fi
    
    return $((total_count - success_count))
}

# Function to test POS BINDU endpoints
test_posbindu_endpoints() {
    print_title "Testing POS BINDU PTM Endpoints"
    
    local success_count=0
    local total_count=0
    
    for service in "${!POSBINDU_ENDPOINTS[@]}"; do
        local endpoint="${POSBINDU_ENDPOINTS[$service]}"
        total_count=$((total_count + 1))
        
        if test_endpoint "$service" "$endpoint"; then
            success_count=$((success_count + 1))
        fi
    done
    
    echo ""
    print_header "POS BINDU PTM Test Results"
    echo "Successful: $success_count/$total_count"
    
    if [ $success_count -eq $total_count ]; then
        print_success "All POS BINDU PTM endpoints are accessible!"
    else
        print_warning "Some POS BINDU PTM endpoints are not accessible"
    fi
    
    return $((total_count - success_count))
}

# Function to test authentication
test_authentication() {
    print_header "Testing Authentication"
    
    # Test Posyandu + authentication
    print_title "Testing Posyandu + Authentication"
    local posyandu_login_response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "admin123"}' \
        http://localhost:8001/api/token/ 2>/dev/null || echo "")
    
    if [ -n "$posyandu_login_response" ] && echo "$posyandu_login_response" | grep -q "access"; then
        print_success "Posyandu + authentication is working"
    else
        print_error "Posyandu + authentication failed"
    fi
    
    # Test POS BINDU authentication
    print_title "Testing POS BINDU PTM Authentication"
    local posbindu_login_response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "admin123"}' \
        http://localhost:8005/api/token/ 2>/dev/null || echo "")
    
    if [ -n "$posbindu_login_response" ] && echo "$posbindu_login_response" | grep -q "access"; then
        print_success "POS BINDU PTM authentication is working"
    else
        print_error "POS BINDU PTM authentication failed"
    fi
}

# Function to test service health
test_service_health() {
    print_header "Testing Service Health"
    
    # Test Posyandu + services
    print_title "Testing Posyandu + Service Health"
    local posyandu_services=(
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
    
    for service_port in "${posyandu_services[@]}"; do
        local service=$(echo $service_port | cut -d: -f1)
        local port=$(echo $service_port | cut -d: -f2)
        
        print_status "Testing $service health..."
        
        if curl -s http://localhost:$port/ >/dev/null 2>&1; then
            print_success "$service is healthy"
        else
            print_error "$service is not healthy"
        fi
    done
    
    # Test POS BINDU services
    print_title "Testing POS BINDU PTM Service Health"
    local posbindu_services=(
        "participant-service:8005"
        "screening-service:8006"
        "examination-service:8007"
        "lab-service:8008"
        "risk-assessment-service:8009"
        "intervention-service:8010"
        "referral-service:8011"
        "reporting-service:8012"
    )
    
    for service_port in "${posbindu_services[@]}"; do
        local service=$(echo $service_port | cut -d: -f1)
        local port=$(echo $service_port | cut -d: -f2)
        
        print_status "Testing $service health..."
        
        if curl -s http://localhost:$port/ >/dev/null 2>&1; then
            print_success "$service is healthy"
        else
            print_error "$service is not healthy"
        fi
    done
}

# Function to test API performance
test_api_performance() {
    print_header "Testing API Performance"
    
    # Test Posyandu + performance
    print_title "Testing Posyandu + API Performance"
    local posyandu_endpoints=(
        "http://localhost:8001/api/auth/"
        "http://localhost:8002/api/posyandu/"
        "http://localhost:8003/api/balita/"
    )
    
    for endpoint in "${posyandu_endpoints[@]}"; do
        print_status "Testing performance for $endpoint"
        
        local start_time=$(date +%s%N)
        curl -s "$endpoint" >/dev/null 2>&1
        local end_time=$(date +%s%N)
        local response_time=$(( (end_time - start_time) / 1000000 ))
        
        if [ $response_time -lt 1000 ]; then
            print_success "Response time: ${response_time}ms (Good)"
        elif [ $response_time -lt 3000 ]; then
            print_warning "Response time: ${response_time}ms (Acceptable)"
        else
            print_error "Response time: ${response_time}ms (Slow)"
        fi
    done
    
    # Test POS BINDU performance
    print_title "Testing POS BINDU PTM API Performance"
    local posbindu_endpoints=(
        "http://localhost:8005/api/participant/"
        "http://localhost:8006/api/screening/"
        "http://localhost:8007/api/examination/"
    )
    
    for endpoint in "${posbindu_endpoints[@]}"; do
        print_status "Testing performance for $endpoint"
        
        local start_time=$(date +%s%N)
        curl -s "$endpoint" >/dev/null 2>&1
        local end_time=$(date +%s%N)
        local response_time=$(( (end_time - start_time) / 1000000 ))
        
        if [ $response_time -lt 1000 ]; then
            print_success "Response time: ${response_time}ms (Good)"
        elif [ $response_time -lt 3000 ]; then
            print_warning "Response time: ${response_time}ms (Acceptable)"
        else
            print_error "Response time: ${response_time}ms (Slow)"
        fi
    done
}

# Function to generate comprehensive test report
generate_test_report() {
    print_header "Generating Comprehensive Test Report"
    
    local report_file="test_report_all_$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "Posyandu + & POS BINDU PTM Comprehensive Test Report"
        echo "Generated: $(date)"
        echo "=================================================="
        echo ""
        
        echo "Posyandu + Service Status:"
        docker-compose ps
        echo ""
        
        echo "POS BINDU PTM Service Status:"
        if [ -d "posbindu" ]; then
            cd posbindu
            docker-compose ps
            cd ..
        else
            echo "POS BINDU directory not found"
        fi
        echo ""
        
        echo "Posyandu + API Endpoint Tests:"
        for service in "${!POSYANDU_ENDPOINTS[@]}"; do
            local endpoint="${POSYANDU_ENDPOINTS[$service]}"
            local response=$(curl -s -w "%{http_code}" -o /dev/null "$endpoint" 2>/dev/null || echo "000")
            echo "$service: $endpoint - HTTP $response"
        done
        echo ""
        
        echo "POS BINDU PTM API Endpoint Tests:"
        for service in "${!POSBINDU_ENDPOINTS[@]}"; do
            local endpoint="${POSBINDU_ENDPOINTS[$service]}"
            local response=$(curl -s -w "%{http_code}" -o /dev/null "$endpoint" 2>/dev/null || echo "000")
            echo "$service: $endpoint - HTTP $response"
        done
        echo ""
        
        echo "System Resources:"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
        
    } > "$report_file"
    
    print_success "Comprehensive test report generated: $report_file"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --all              Test all applications"
    echo "  --posyandu         Test only Posyandu + application"
    echo "  --posbindu         Test only POS BINDU PTM application"
    echo "  --auth             Test authentication"
    echo "  --health           Test service health"
    echo "  --performance      Test API performance"
    echo "  --report           Generate comprehensive test report"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --all           Test all applications"
    echo "  $0 --posyandu      Test only Posyandu +"
    echo "  $0 --posbindu      Test only POS BINDU PTM"
    echo "  $0 --auth          Test authentication"
    echo "  $0 --health        Test service health"
    echo "  $0 --report        Generate test report"
}

# Main execution
main() {
    echo "============================================================================="
    echo "🧪 Testing All Applications (Posyandu + & POS BINDU PTM)"
    echo "============================================================================="
    echo ""
    
    # Parse command line arguments
    TEST_ALL=false
    TEST_POSYANDU=false
    TEST_POSBINDU=false
    TEST_AUTH=false
    TEST_HEALTH=false
    TEST_PERFORMANCE=false
    GENERATE_REPORT=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)
                TEST_ALL=true
                shift
                ;;
            --posyandu)
                TEST_POSYANDU=true
                shift
                ;;
            --posbindu)
                TEST_POSBINDU=true
                shift
                ;;
            --auth)
                TEST_AUTH=true
                shift
                ;;
            --health)
                TEST_HEALTH=true
                shift
                ;;
            --performance)
                TEST_PERFORMANCE=true
                shift
                ;;
            --report)
                GENERATE_REPORT=true
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
    if [ "$TEST_ALL" = true ]; then
        test_posyandu_endpoints
        test_posbindu_endpoints
        test_authentication
        test_service_health
        test_api_performance
    elif [ "$TEST_POSYANDU" = true ]; then
        test_posyandu_endpoints
    elif [ "$TEST_POSBINDU" = true ]; then
        test_posbindu_endpoints
    elif [ "$TEST_AUTH" = true ]; then
        test_authentication
    elif [ "$TEST_HEALTH" = true ]; then
        test_service_health
    elif [ "$TEST_PERFORMANCE" = true ]; then
        test_api_performance
    elif [ "$GENERATE_REPORT" = true ]; then
        generate_test_report
    else
        # Default: test all applications
        test_posyandu_endpoints
        test_posbindu_endpoints
        test_authentication
        test_service_health
        test_api_performance
    fi
    
    print_success "Testing completed!"
}

# Run main function
main "$@"