#!/bin/bash

# Test POS BINDU PTM Microservices
echo "🧪 Testing POS BINDU PTM Microservices"
echo "======================================"
echo ""

# Base URL
BASE_URL="http://localhost:8080"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local service_name="$1"
    local endpoint="$2"
    local expected_status="$3"
    
    echo -n "Testing $service_name... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$endpoint")
    
    if [ "$response" = "$expected_status" ]; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED (Status: $response)${NC}"
        return 1
    fi
}

echo "🔍 Testing Basic Service Health..."
echo ""

# Test 1: API Gateway Health
test_endpoint "API Gateway Health" "$BASE_URL/health" "200"

# Test 2: Participant Service
test_endpoint "Participant Service" "$BASE_URL/api/participant/participant/" "200"

# Test 3: Screening Service
test_endpoint "Screening Service" "$BASE_URL/api/screening/visit/" "200"

# Test 4: Examination Service
test_endpoint "Examination Service" "$BASE_URL/api/examination/vital-sign/" "200"

# Test 5: Lab Service
test_endpoint "Lab Service" "$BASE_URL/api/lab/result/" "200"

# Test 6: Risk Assessment Service
test_endpoint "Risk Assessment Service" "$BASE_URL/api/risk-assessment/assessment/" "200"

# Test 7: Intervention Service
test_endpoint "Intervention Service" "$BASE_URL/api/intervention/intervention/" "200"

# Test 8: Referral Service
test_endpoint "Referral Service" "$BASE_URL/api/referral/referral/" "200"

# Test 9: Reporting Service
test_endpoint "Reporting Service" "$BASE_URL/api/reporting/report-log/" "200"

echo ""
echo "📊 Testing Statistics Endpoints..."
echo ""

# Test Statistics Endpoints
test_endpoint "Participant Statistics" "$BASE_URL/api/participant/participant/statistics/" "200"
test_endpoint "Screening Statistics" "$BASE_URL/api/screening/visit/statistics/" "200"
test_endpoint "Examination Statistics" "$BASE_URL/api/examination/vital-sign/statistics/" "200"
test_endpoint "Lab Statistics" "$BASE_URL/api/lab/result/statistics/" "200"
test_endpoint "Risk Assessment Statistics" "$BASE_URL/api/risk-assessment/assessment/statistics/" "200"
test_endpoint "Intervention Statistics" "$BASE_URL/api/intervention/intervention/statistics/" "200"
test_endpoint "Referral Statistics" "$BASE_URL/api/referral/referral/statistics/" "200"
test_endpoint "Reporting Statistics" "$BASE_URL/api/reporting/report-log/statistics/" "200"

echo ""
echo "🔍 Testing Advanced Endpoints..."
echo ""

# Test Advanced Endpoints
test_endpoint "Screening by Participant" "$BASE_URL/api/screening/visit/by_participant/?participant_id=1" "200"
test_endpoint "Examination by Visit" "$BASE_URL/api/examination/vital-sign/by_visit/?visit_id=1" "200"
test_endpoint "Lab by Visit" "$BASE_URL/api/lab/result/by_visit/?visit_id=1" "200"
test_endpoint "Risk Assessment by Visit" "$BASE_URL/api/risk-assessment/assessment/by_visit/?visit_id=1" "200"
test_endpoint "Intervention by Visit" "$BASE_URL/api/intervention/intervention/by_visit/?visit_id=1" "200"
test_endpoint "Referral by Visit" "$BASE_URL/api/referral/referral/by_visit/?visit_id=1" "200"

echo ""
echo "🌐 Testing Frontend..."
echo ""

# Test Frontend
test_endpoint "Frontend" "http://localhost:3001" "200"

echo ""
echo "📋 Service Status Summary"
echo "========================"

# Count successful tests
total_tests=0
passed_tests=0

# Test all services again and count
services=(
    "API Gateway:$BASE_URL/health:200"
    "Participant Service:$BASE_URL/api/participant/participant/:200"
    "Screening Service:$BASE_URL/api/screening/visit/:200"
    "Examination Service:$BASE_URL/api/examination/vital-sign/:200"
    "Lab Service:$BASE_URL/api/lab/result/:200"
    "Risk Assessment Service:$BASE_URL/api/risk-assessment/assessment/:200"
    "Intervention Service:$BASE_URL/api/intervention/intervention/:200"
    "Referral Service:$BASE_URL/api/referral/referral/:200"
    "Reporting Service:$BASE_URL/api/reporting/report-log/:200"
    "Frontend:http://localhost:3001:200"
)

for service in "${services[@]}"; do
    IFS=':' read -r name endpoint expected <<< "$service"
    total_tests=$((total_tests + 1))
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$endpoint")
    if [ "$response" = "$expected" ]; then
        echo -e "✅ $name: ${GREEN}RUNNING${NC}"
        passed_tests=$((passed_tests + 1))
    else
        echo -e "❌ $name: ${RED}FAILED${NC} (Status: $response)"
    fi
done

echo ""
echo "📊 Test Results"
echo "==============="
echo -e "Total Tests: $total_tests"
echo -e "Passed: ${GREEN}$passed_tests${NC}"
echo -e "Failed: ${RED}$((total_tests - passed_tests))${NC}"

if [ $passed_tests -eq $total_tests ]; then
    echo -e "\n🎉 ${GREEN}All POS BINDU PTM services are running successfully!${NC}"
    echo -e "🌐 ${BLUE}Frontend: http://localhost:3001${NC}"
    echo -e "🔗 ${BLUE}API: http://localhost:8080${NC}"
else
    echo -e "\n⚠️  ${YELLOW}Some services are not running properly.${NC}"
    echo -e "Check the logs with: ${BLUE}docker-compose logs${NC}"
fi

echo ""
echo "🔧 Useful Commands:"
echo "==================="
echo "• View logs: docker-compose logs -f [service-name]"
echo "• Restart service: docker-compose restart [service-name]"
echo "• Stop all: docker-compose down"
echo "• Start all: docker-compose up -d"
echo "• Rebuild: docker-compose up --build -d"
