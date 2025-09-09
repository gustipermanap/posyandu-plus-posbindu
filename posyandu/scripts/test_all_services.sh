#!/bin/bash

# Test All Services Script
# Testing semua 9 microservices Posyandu +

echo "🚀 Testing All Posyandu + Microservices"
echo "========================================"
echo ""

# Base URL
BASE_URL="http://localhost:80"

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

# Function to test with data
test_endpoint_with_data() {
    local service_name="$1"
    local endpoint="$2"
    local expected_status="$3"
    
    echo -n "Testing $service_name with data... "
    
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

# Test 2: Auth Service
test_endpoint "Auth Service" "$BASE_URL/api/auth/" "200"

# Test 3: Posyandu Service
test_endpoint "Posyandu Service" "$BASE_URL/api/posyandu/" "200"

# Test 4: Balita Service
test_endpoint "Balita Service" "$BASE_URL/api/balita/pemeriksaan/" "200"

# Test 5: Ibu Hamil Service
test_endpoint "Ibu Hamil Service" "$BASE_URL/api/ibu-hamil/pemeriksaan/" "200"

# Test 6: Imunisasi Service
test_endpoint "Imunisasi Service" "$BASE_URL/api/imunisasi/jadwal/" "200"

# Test 7: KB Service
test_endpoint "KB Service" "$BASE_URL/api/kb/metode/" "200"

# Test 8: Vitamin Service
test_endpoint "Vitamin Service" "$BASE_URL/api/vitamin/jenis/" "200"

# Test 9: Rujukan Service
test_endpoint "Rujukan Service" "$BASE_URL/api/rujukan/fasilitas/" "200"

# Test 10: Laporan Service
test_endpoint "Laporan Service" "$BASE_URL/api/laporan/template/" "200"

echo ""
echo "📊 Testing Statistics Endpoints..."
echo ""

# Test Statistics Endpoints
test_endpoint "Balita Statistics" "$BASE_URL/api/balita/pemeriksaan/statistics/" "200"
test_endpoint "Ibu Hamil Statistics" "$BASE_URL/api/ibu-hamil/pemeriksaan/statistics/" "200"
test_endpoint "Imunisasi Statistics" "$BASE_URL/api/imunisasi/pencatatan/statistics/" "200"
test_endpoint "KB Statistics" "$BASE_URL/api/kb/pencatatan/statistics/" "200"
test_endpoint "Vitamin Statistics" "$BASE_URL/api/vitamin/pemberian/statistics/" "200"
test_endpoint "Rujukan Statistics" "$BASE_URL/api/rujukan/rujukan/statistics/" "200"
test_endpoint "Laporan Statistics" "$BASE_URL/api/laporan/template/statistics/" "200"

echo ""
echo "🔍 Testing Advanced Endpoints..."
echo ""

# Test Advanced Endpoints
test_endpoint "Imunisasi by Usia" "$BASE_URL/api/imunisasi/jadwal/by_usia/?usia=12" "200"
test_endpoint "KB by Metode" "$BASE_URL/api/kb/pencatatan/by_metode/?metode=pil" "200"
test_endpoint "Vitamin by Jenis" "$BASE_URL/api/vitamin/pemberian/by_jenis/?jenis=vitamin_a" "200"
test_endpoint "Rujukan by Status" "$BASE_URL/api/rujukan/rujukan/by_status/?status=dikirim" "200"
test_endpoint "Laporan by Kategori" "$BASE_URL/api/laporan/template/by_kategori/?kategori_laporan=balita" "200"

echo ""
echo "🌐 Testing Frontend..."
echo ""

# Test Frontend
test_endpoint "Frontend" "http://localhost:3000" "200"

echo ""
echo "📋 Service Status Summary"
echo "========================"

# Count successful tests
total_tests=0
passed_tests=0

# Test all services again and count
services=(
    "API Gateway:$BASE_URL/health:200"
    "Auth Service:$BASE_URL/api/auth/:200"
    "Posyandu Service:$BASE_URL/api/posyandu/:200"
    "Balita Service:$BASE_URL/api/balita/pemeriksaan/:200"
    "Ibu Hamil Service:$BASE_URL/api/ibu-hamil/pemeriksaan/:200"
    "Imunisasi Service:$BASE_URL/api/imunisasi/jadwal/:200"
    "KB Service:$BASE_URL/api/kb/metode/:200"
    "Vitamin Service:$BASE_URL/api/vitamin/jenis/:200"
    "Rujukan Service:$BASE_URL/api/rujukan/fasilitas/:200"
    "Laporan Service:$BASE_URL/api/laporan/template/:200"
    "Frontend:http://localhost:3000:200"
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
    echo -e "\n🎉 ${GREEN}All services are running successfully!${NC}"
    echo -e "🌐 ${BLUE}Frontend: http://localhost:3000${NC}"
    echo -e "🔗 ${BLUE}API: http://localhost:80${NC}"
    echo -e "👤 ${BLUE}Admin: admin/admin123${NC}"
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
