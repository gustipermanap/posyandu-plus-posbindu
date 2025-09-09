#!/bin/bash

# Script untuk testing API endpoints Posyandu

echo "🧪 Testing Posyandu API Endpoints..."

# Base URL
BASE_URL="http://localhost:80"

# Test Health Check
echo "1. Testing Health Check..."
curl -s "$BASE_URL/health" && echo " ✅" || echo " ❌"

# Test Auth Service
echo "2. Testing Auth Service..."
curl -s "$BASE_URL/api/auth/health/" && echo " ✅" || echo " ❌"

# Test Posyandu Service
echo "3. Testing Posyandu Service..."
curl -s "$BASE_URL/api/posyandu/" && echo " ✅" || echo " ❌"

# Test Balita Service
echo "4. Testing Balita Service..."
curl -s "$BASE_URL/api/balita/" && echo " ✅" || echo " ❌"

# Test Ibu Hamil Service
echo "5. Testing Ibu Hamil Service..."
curl -s "$BASE_URL/api/ibu-hamil/" && echo " ✅" || echo " ❌"

# Test Imunisasi Service
echo "6. Testing Imunisasi Service..."
curl -s "$BASE_URL/api/imunisasi/" && echo " ✅" || echo " ❌"

# Test KB Service
echo "7. Testing KB Service..."
curl -s "$BASE_URL/api/kb/" && echo " ✅" || echo " ❌"

# Test Vitamin Service
echo "8. Testing Vitamin Service..."
curl -s "$BASE_URL/api/vitamin/" && echo " ✅" || echo " ❌"

# Test Rujukan Service
echo "9. Testing Rujukan Service..."
curl -s "$BASE_URL/api/rujukan/" && echo " ✅" || echo " ❌"

# Test Laporan Service
echo "10. Testing Laporan Service..."
curl -s "$BASE_URL/api/laporan/" && echo " ✅" || echo " ❌"

# Test specific endpoints
echo ""
echo "🔍 Testing specific endpoints..."

# Test Balita Statistics
echo "11. Testing Balita Statistics..."
curl -s "$BASE_URL/api/balita/pemeriksaan/statistics/" && echo " ✅" || echo " ❌"

# Test Ibu Hamil Statistics
echo "12. Testing Ibu Hamil Statistics..."
curl -s "$BASE_URL/api/ibu-hamil/pemeriksaan/statistics/" && echo " ✅" || echo " ❌"

# Test Imunisasi Statistics
echo "13. Testing Imunisasi Statistics..."
curl -s "$BASE_URL/api/imunisasi/pencatatan/statistics/" && echo " ✅" || echo " ❌"

# Test KB Statistics
echo "14. Testing KB Statistics..."
curl -s "$BASE_URL/api/kb/pencatatan/statistics/" && echo " ✅" || echo " ❌"

# Test Vitamin Statistics
echo "15. Testing Vitamin Statistics..."
curl -s "$BASE_URL/api/vitamin/pemberian/statistics/" && echo " ✅" || echo " ❌"

# Test Rujukan Statistics
echo "16. Testing Rujukan Statistics..."
curl -s "$BASE_URL/api/rujukan/rujukan/statistics/" && echo " ✅" || echo " ❌"

# Test Laporan Statistics
echo "17. Testing Laporan Statistics..."
curl -s "$BASE_URL/api/laporan/template/statistics/" && echo " ✅" || echo " ❌"

echo ""
echo "✅ API testing completed!"
echo ""
echo "📊 To view detailed responses, run:"
echo "  curl -s $BASE_URL/api/[service]/[endpoint]/ | jq"
echo ""
echo "🔍 To test with specific parameters:"
echo "  curl -s '$BASE_URL/api/balita/pemeriksaan/by_balita/?balita_id=1'"
echo "  curl -s '$BASE_URL/api/ibu-hamil/pemeriksaan/by_ibu_hamil/?ibu_hamil_id=1'"
echo "  curl -s '$BASE_URL/api/imunisasi/jadwal/by_usia/?usia_bulan=12'"