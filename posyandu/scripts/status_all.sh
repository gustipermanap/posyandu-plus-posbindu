#!/bin/bash

# Script untuk check status semua services Posyandu+ dan POS BINDU PTM

echo "📊 Service Status - Posyandu+ & POS BINDU PTM"
echo "============================================="

# Function untuk check Posyandu+ services
check_posyandu() {
    echo "🏥 Posyandu+ Services Status:"
    echo "============================="
    
    # Check if containers are running
    if docker compose ps | grep -q "Up"; then
        echo "✅ Posyandu+ containers are running"
        
        # Show running containers
        echo ""
        echo "📋 Running Containers:"
        docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
        
        # Check API endpoints
        echo ""
        echo "🔗 API Endpoints Status:"
        
        # Auth Service
        if curl -s http://localhost:8001/api/auth/ > /dev/null 2>&1; then
            echo "  ✅ Auth Service (Port 8001) - OK"
        else
            echo "  ❌ Auth Service (Port 8001) - Not responding"
        fi
        
        # Posyandu Service
        if curl -s http://localhost:8002/api/posyandu/ > /dev/null 2>&1; then
            echo "  ✅ Posyandu Service (Port 8002) - OK"
        else
            echo "  ❌ Posyandu Service (Port 8002) - Not responding"
        fi
        
        # Balita Service
        if curl -s http://localhost:8003/api/balita/ > /dev/null 2>&1; then
            echo "  ✅ Balita Service (Port 8003) - OK"
        else
            echo "  ❌ Balita Service (Port 8003) - Not responding"
        fi
        
        # Ibu Hamil Service
        if curl -s http://localhost:8004/api/ibu-hamil/ > /dev/null 2>&1; then
            echo "  ✅ Ibu Hamil Service (Port 8004) - OK"
        else
            echo "  ❌ Ibu Hamil Service (Port 8004) - Not responding"
        fi
        
        # Imunisasi Service
        if curl -s http://localhost:8005/api/imunisasi/ > /dev/null 2>&1; then
            echo "  ✅ Imunisasi Service (Port 8005) - OK"
        else
            echo "  ❌ Imunisasi Service (Port 8005) - Not responding"
        fi
        
        # KB Service
        if curl -s http://localhost:8006/api/kb/ > /dev/null 2>&1; then
            echo "  ✅ KB Service (Port 8006) - OK"
        else
            echo "  ❌ KB Service (Port 8006) - Not responding"
        fi
        
        # Vitamin Service
        if curl -s http://localhost:8007/api/vitamin/ > /dev/null 2>&1; then
            echo "  ✅ Vitamin Service (Port 8007) - OK"
        else
            echo "  ❌ Vitamin Service (Port 8007) - Not responding"
        fi
        
        # Rujukan Service
        if curl -s http://localhost:8008/api/rujukan/ > /dev/null 2>&1; then
            echo "  ✅ Rujukan Service (Port 8008) - OK"
        else
            echo "  ❌ Rujukan Service (Port 8008) - Not responding"
        fi
        
        # Laporan Service
        if curl -s http://localhost:8009/api/laporan/ > /dev/null 2>&1; then
            echo "  ✅ Laporan Service (Port 8009) - OK"
        else
            echo "  ❌ Laporan Service (Port 8009) - Not responding"
        fi
        
        # API Gateway
        if curl -s http://localhost/ > /dev/null 2>&1; then
            echo "  ✅ API Gateway (Port 80) - OK"
        else
            echo "  ❌ API Gateway (Port 80) - Not responding"
        fi
        
        # Frontend
        if curl -s http://localhost:3000/ > /dev/null 2>&1; then
            echo "  ✅ Frontend (Port 3000) - OK"
        else
            echo "  ❌ Frontend (Port 3000) - Not responding"
        fi
        
    else
        echo "❌ Posyandu+ containers are not running"
    fi
    
    echo ""
}

# Function untuk check POS BINDU PTM services
check_posbindu() {
    echo "🏥 POS BINDU PTM Services Status:"
    echo "================================="
    
    # Check if containers are running
    if cd posbindu && docker compose ps | grep -q "Up"; then
        echo "✅ POS BINDU PTM containers are running"
        
        # Show running containers
        echo ""
        echo "📋 Running Containers:"
        docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
        
        # Check API endpoints
        echo ""
        echo "🔗 API Endpoints Status:"
        
        # Participant Service
        if curl -s http://localhost:8005/api/participant/ > /dev/null 2>&1; then
            echo "  ✅ Participant Service (Port 8005) - OK"
        else
            echo "  ❌ Participant Service (Port 8005) - Not responding"
        fi
        
        # Screening Service
        if curl -s http://localhost:8006/api/screening/ > /dev/null 2>&1; then
            echo "  ✅ Screening Service (Port 8006) - OK"
        else
            echo "  ❌ Screening Service (Port 8006) - Not responding"
        fi
        
        # Examination Service
        if curl -s http://localhost:8007/api/examination/ > /dev/null 2>&1; then
            echo "  ✅ Examination Service (Port 8007) - OK"
        else
            echo "  ❌ Examination Service (Port 8007) - Not responding"
        fi
        
        # Lab Service
        if curl -s http://localhost:8008/api/lab/ > /dev/null 2>&1; then
            echo "  ✅ Lab Service (Port 8008) - OK"
        else
            echo "  ❌ Lab Service (Port 8008) - Not responding"
        fi
        
        # Risk Assessment Service
        if curl -s http://localhost:8009/api/risk-assessment/ > /dev/null 2>&1; then
            echo "  ✅ Risk Assessment Service (Port 8009) - OK"
        else
            echo "  ❌ Risk Assessment Service (Port 8009) - Not responding"
        fi
        
        # Intervention Service
        if curl -s http://localhost:8010/api/intervention/ > /dev/null 2>&1; then
            echo "  ✅ Intervention Service (Port 8010) - OK"
        else
            echo "  ❌ Intervention Service (Port 8010) - Not responding"
        fi
        
        # Referral Service
        if curl -s http://localhost:8011/api/referral/ > /dev/null 2>&1; then
            echo "  ✅ Referral Service (Port 8011) - OK"
        else
            echo "  ❌ Referral Service (Port 8011) - Not responding"
        fi
        
        # Reporting Service
        if curl -s http://localhost:8012/api/reporting/ > /dev/null 2>&1; then
            echo "  ✅ Reporting Service (Port 8012) - OK"
        else
            echo "  ❌ Reporting Service (Port 8012) - Not responding"
        fi
        
        # API Gateway
        if curl -s http://localhost:8080/ > /dev/null 2>&1; then
            echo "  ✅ API Gateway (Port 8080) - OK"
        else
            echo "  ❌ API Gateway (Port 8080) - Not responding"
        fi
        
        # Frontend
        if curl -s http://localhost:3001/ > /dev/null 2>&1; then
            echo "  ✅ Frontend (Port 3001) - OK"
        else
            echo "  ❌ Frontend (Port 3001) - Not responding"
        fi
        
    else
        echo "❌ POS BINDU PTM containers are not running"
    fi
    
    cd ..
    echo ""
}

# Function untuk show summary
show_summary() {
    echo "📊 Summary:"
    echo "==========="
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
    echo ""
}

# Main execution
main() {
    # Check Posyandu+ services
    check_posyandu
    
    # Check POS BINDU PTM services
    check_posbindu
    
    # Show summary
    show_summary
}

# Run main function
main

echo "📊 Status check completed!"
