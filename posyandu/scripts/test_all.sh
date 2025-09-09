#!/bin/bash

# Script untuk test semua services Posyandu+ dan POS BINDU PTM

echo "🧪 Testing All Services - Posyandu+ & POS BINDU PTM"
echo "=================================================="

# Function untuk test Posyandu+ services
test_posyandu() {
    echo "🏥 Testing Posyandu+ Services..."
    echo "==============================="
    
    # Test API endpoints
    echo "🔗 Testing API Endpoints:"
    
    # Auth Service
    echo "  - Testing Auth Service..."
    if curl -s http://localhost:8001/api/auth/ > /dev/null 2>&1; then
        echo "    ✅ Auth Service - OK"
    else
        echo "    ❌ Auth Service - Failed"
    fi
    
    # Posyandu Service
    echo "  - Testing Posyandu Service..."
    if curl -s http://localhost:8002/api/posyandu/ > /dev/null 2>&1; then
        echo "    ✅ Posyandu Service - OK"
    else
        echo "    ❌ Posyandu Service - Failed"
    fi
    
    # Balita Service
    echo "  - Testing Balita Service..."
    if curl -s http://localhost:8003/api/balita/ > /dev/null 2>&1; then
        echo "    ✅ Balita Service - OK"
    else
        echo "    ❌ Balita Service - Failed"
    fi
    
    # Ibu Hamil Service
    echo "  - Testing Ibu Hamil Service..."
    if curl -s http://localhost:8004/api/ibu-hamil/ > /dev/null 2>&1; then
        echo "    ✅ Ibu Hamil Service - OK"
    else
        echo "    ❌ Ibu Hamil Service - Failed"
    fi
    
    # Imunisasi Service
    echo "  - Testing Imunisasi Service..."
    if curl -s http://localhost:8005/api/imunisasi/ > /dev/null 2>&1; then
        echo "    ✅ Imunisasi Service - OK"
    else
        echo "    ❌ Imunisasi Service - Failed"
    fi
    
    # KB Service
    echo "  - Testing KB Service..."
    if curl -s http://localhost:8006/api/kb/ > /dev/null 2>&1; then
        echo "    ✅ KB Service - OK"
    else
        echo "    ❌ KB Service - Failed"
    fi
    
    # Vitamin Service
    echo "  - Testing Vitamin Service..."
    if curl -s http://localhost:8007/api/vitamin/ > /dev/null 2>&1; then
        echo "    ✅ Vitamin Service - OK"
    else
        echo "    ❌ Vitamin Service - Failed"
    fi
    
    # Rujukan Service
    echo "  - Testing Rujukan Service..."
    if curl -s http://localhost:8008/api/rujukan/ > /dev/null 2>&1; then
        echo "    ✅ Rujukan Service - OK"
    else
        echo "    ❌ Rujukan Service - Failed"
    fi
    
    # Laporan Service
    echo "  - Testing Laporan Service..."
    if curl -s http://localhost:8009/api/laporan/ > /dev/null 2>&1; then
        echo "    ✅ Laporan Service - OK"
    else
        echo "    ❌ Laporan Service - Failed"
    fi
    
    # API Gateway
    echo "  - Testing API Gateway..."
    if curl -s http://localhost/ > /dev/null 2>&1; then
        echo "    ✅ API Gateway - OK"
    else
        echo "    ❌ API Gateway - Failed"
    fi
    
    # Frontend
    echo "  - Testing Frontend..."
    if curl -s http://localhost:3000/ > /dev/null 2>&1; then
        echo "    ✅ Frontend - OK"
    else
        echo "    ❌ Frontend - Failed"
    fi
    
    echo ""
}

# Function untuk test POS BINDU PTM services
test_posbindu() {
    echo "🏥 Testing POS BINDU PTM Services..."
    echo "===================================="
    
    # Test API endpoints
    echo "🔗 Testing API Endpoints:"
    
    # Participant Service
    echo "  - Testing Participant Service..."
    if curl -s http://localhost:8005/api/participant/ > /dev/null 2>&1; then
        echo "    ✅ Participant Service - OK"
    else
        echo "    ❌ Participant Service - Failed"
    fi
    
    # Screening Service
    echo "  - Testing Screening Service..."
    if curl -s http://localhost:8006/api/screening/ > /dev/null 2>&1; then
        echo "    ✅ Screening Service - OK"
    else
        echo "    ❌ Screening Service - Failed"
    fi
    
    # Examination Service
    echo "  - Testing Examination Service..."
    if curl -s http://localhost:8007/api/examination/ > /dev/null 2>&1; then
        echo "    ✅ Examination Service - OK"
    else
        echo "    ❌ Examination Service - Failed"
    fi
    
    # Lab Service
    echo "  - Testing Lab Service..."
    if curl -s http://localhost:8008/api/lab/ > /dev/null 2>&1; then
        echo "    ✅ Lab Service - OK"
    else
        echo "    ❌ Lab Service - Failed"
    fi
    
    # Risk Assessment Service
    echo "  - Testing Risk Assessment Service..."
    if curl -s http://localhost:8009/api/risk-assessment/ > /dev/null 2>&1; then
        echo "    ✅ Risk Assessment Service - OK"
    else
        echo "    ❌ Risk Assessment Service - Failed"
    fi
    
    # Intervention Service
    echo "  - Testing Intervention Service..."
    if curl -s http://localhost:8010/api/intervention/ > /dev/null 2>&1; then
        echo "    ✅ Intervention Service - OK"
    else
        echo "    ❌ Intervention Service - Failed"
    fi
    
    # Referral Service
    echo "  - Testing Referral Service..."
    if curl -s http://localhost:8011/api/referral/ > /dev/null 2>&1; then
        echo "    ✅ Referral Service - OK"
    else
        echo "    ❌ Referral Service - Failed"
    fi
    
    # Reporting Service
    echo "  - Testing Reporting Service..."
    if curl -s http://localhost:8012/api/reporting/ > /dev/null 2>&1; then
        echo "    ✅ Reporting Service - OK"
    else
        echo "    ❌ Reporting Service - Failed"
    fi
    
    # API Gateway
    echo "  - Testing API Gateway..."
    if curl -s http://localhost:8080/ > /dev/null 2>&1; then
        echo "    ✅ API Gateway - OK"
    else
        echo "    ❌ API Gateway - Failed"
    fi
    
    # Frontend
    echo "  - Testing Frontend..."
    if curl -s http://localhost:3001/ > /dev/null 2>&1; then
        echo "    ✅ Frontend - OK"
    else
        echo "    ❌ Frontend - Failed"
    fi
    
    echo ""
}

# Function untuk show summary
show_summary() {
    echo "📊 Test Summary:"
    echo "==============="
    echo ""
    echo "🌐 Access URLs:"
    echo "  📱 Posyandu+ Frontend: http://localhost:3000"
    echo "  🔗 Posyandu+ API: http://localhost"
    echo "  📱 POS BINDU PTM Frontend: http://localhost:3001"
    echo "  🔗 POS BINDU PTM API: http://localhost:8080"
    echo ""
    echo "🔑 Demo Login:"
    echo "  Username: admin"
    echo "  Password: admin123"
    echo ""
    echo "🛠️ Management Commands:"
    echo "  Start all: ./start_all.sh"
    echo "  Stop all: ./stop_all.sh"
    echo "  Restart all: ./restart_all.sh"
    echo "  Check status: ./status_all.sh"
    echo "  View logs: ./logs_all.sh"
    echo ""
}

# Main execution
main() {
    # Test Posyandu+ services
    test_posyandu
    
    # Test POS BINDU PTM services
    test_posbindu
    
    # Show summary
    show_summary
}

# Run main function
main

echo "🧪 All tests completed!"
