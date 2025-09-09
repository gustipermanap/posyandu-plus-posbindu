#!/bin/bash

# Script untuk melihat logs semua services Posyandu+ dan POS BINDU PTM

echo "📋 Service Logs - Posyandu+ & POS BINDU PTM"
echo "==========================================="

# Function untuk show logs
show_logs() {
    echo "📋 Showing logs for all services..."
    echo "=================================="
    
    # Show Posyandu+ logs
    echo "🏥 Posyandu+ Services Logs:"
    echo "==========================="
    docker-compose logs -f --tail=50
}

# Function untuk show specific service logs
show_specific_logs() {
    local service=$1
    
    if [ -z "$service" ]; then
        echo "❌ Please specify a service name"
        echo ""
        echo "Available services:"
        echo "  Posyandu+: auth-service, posyandu-service, balita-service, ibu-hamil-service, imunisasi-service, kb-service, vitamin-service, rujukan-service, laporan-service, api-gateway, frontend"
        echo "  POS BINDU PTM: participant-service, screening-service, examination-service, lab-service, risk-assessment-service, intervention-service, referral-service, reporting-service, api-gateway, posbindu-frontend"
        echo ""
        echo "Usage: ./logs_all.sh [service-name]"
        return 1
    fi
    
    echo "📋 Showing logs for $service..."
    echo "=============================="
    
    # Check if it's a Posyandu+ service
    if docker-compose ps | grep -q "$service"; then
        docker-compose logs -f --tail=50 "$service"
    # Check if it's a POS BINDU PTM service
    elif cd posbindu && docker-compose ps | grep -q "$service"; then
        docker-compose logs -f --tail=50 "$service"
        cd ..
    else
        echo "❌ Service $service not found"
        echo ""
        echo "Available services:"
        echo "  Posyandu+: auth-service, posyandu-service, balita-service, ibu-hamil-service, imunisasi-service, kb-service, vitamin-service, rujukan-service, laporan-service, api-gateway, frontend"
        echo "  POS BINDU PTM: participant-service, screening-service, examination-service, lab-service, risk-assessment-service, intervention-service, referral-service, reporting-service, api-gateway, posbindu-frontend"
        return 1
    fi
}

# Function untuk show help
show_help() {
    echo "📋 Service Logs - Posyandu+ & POS BINDU PTM"
    echo "==========================================="
    echo ""
    echo "Usage:"
    echo "  ./logs_all.sh                    # Show all Posyandu+ logs"
    echo "  ./logs_all.sh [service-name]     # Show specific service logs"
    echo "  ./logs_all.sh --help             # Show this help"
    echo ""
    echo "Available services:"
    echo "  Posyandu+:"
    echo "    auth-service, posyandu-service, balita-service, ibu-hamil-service"
    echo "    imunisasi-service, kb-service, vitamin-service, rujukan-service"
    echo "    laporan-service, api-gateway, frontend"
    echo ""
    echo "  POS BINDU PTM:"
    echo "    participant-service, screening-service, examination-service"
    echo "    lab-service, risk-assessment-service, intervention-service"
    echo "    referral-service, reporting-service, api-gateway, posbindu-frontend"
    echo ""
    echo "Examples:"
    echo "  ./logs_all.sh auth-service"
    echo "  ./logs_all.sh participant-service"
    echo "  ./logs_all.sh api-gateway"
    echo ""
}

# Main execution
main() {
    # Check for help flag
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_help
        return 0
    fi
    
    # Check if specific service is requested
    if [ -n "$1" ]; then
        show_specific_logs "$1"
    else
        show_logs
    fi
}

# Run main function
main "$@"
