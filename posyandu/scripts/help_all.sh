#!/bin/bash

# Script untuk menampilkan help semua services Posyandu+ dan POS BINDU PTM

echo "🆘 Help - Posyandu+ & POS BINDU PTM Management"
echo "============================================="

# Function untuk show help
show_help() {
    echo "🆘 Available Commands:"
    echo "====================="
    echo ""
    echo "🚀 Service Management:"
    echo "  ./start_all.sh          # Start all services (Posyandu+ & POS BINDU PTM)"
    echo "  ./stop_all.sh           # Stop all services"
    echo "  ./restart_all.sh        # Restart all services"
    echo "  ./status_all.sh         # Check status of all services"
    echo "  ./test_all.sh           # Test all services"
    echo ""
    echo "📋 Logs & Monitoring:"
    echo "  ./logs_all.sh           # View logs for all Posyandu+ services"
    echo "  ./logs_all.sh [service] # View logs for specific service"
    echo "  ./logs_all.sh --help    # Show logs help"
    echo ""
    echo "🧹 Cleanup:"
    echo "  ./cleanup_all.sh        # Full cleanup (stop + clean all)"
    echo "  ./cleanup_all.sh --stop # Stop all services only"
    echo "  ./cleanup_all.sh --images # Clean images only"
    echo "  ./cleanup_all.sh --help # Show cleanup help"
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
    echo "📊 Service Ports:"
    echo "  Posyandu+ Services:"
    echo "    Auth Service: 8001"
    echo "    Posyandu Service: 8002"
    echo "    Balita Service: 8003"
    echo "    Ibu Hamil Service: 8004"
    echo "    Imunisasi Service: 8005"
    echo "    KB Service: 8006"
    echo "    Vitamin Service: 8007"
    echo "    Rujukan Service: 8008"
    echo "    Laporan Service: 8009"
    echo "    API Gateway: 80"
    echo "    Frontend: 3000"
    echo ""
    echo "  POS BINDU PTM Services:"
    echo "    Participant Service: 8005"
    echo "    Screening Service: 8006"
    echo "    Examination Service: 8007"
    echo "    Lab Service: 8008"
    echo "    Risk Assessment Service: 8009"
    echo "    Intervention Service: 8010"
    echo "    Referral Service: 8011"
    echo "    Reporting Service: 8012"
    echo "    API Gateway: 8080"
    echo "    Frontend: 3001"
    echo ""
    echo "🛠️ Quick Start:"
    echo "  1. ./start_all.sh        # Start all services"
    echo "  2. ./status_all.sh       # Check if everything is running"
    echo "  3. Open browser and go to http://localhost:3000 or http://localhost:3001"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "  If services fail to start:"
    echo "    1. ./stop_all.sh       # Stop all services"
    echo "    2. ./cleanup_all.sh    # Clean up everything"
    echo "    3. ./start_all.sh      # Start fresh"
    echo ""
    echo "  If you see port conflicts:"
    echo "    1. ./stop_all.sh       # Stop all services"
    echo "    2. ./start_all.sh      # Start again"
    echo ""
    echo "  If you want to see what's happening:"
    echo "    ./logs_all.sh          # View all logs"
    echo "    ./status_all.sh        # Check service status"
    echo ""
    echo "📚 Documentation:"
    echo "  README.md               # Main documentation"
    echo "  posyandu/README.md      # Posyandu+ documentation"
    echo "  posbindu/README.md      # POS BINDU PTM documentation"
    echo ""
    echo "🆘 Need Help?"
    echo "  Check the documentation files or run specific help commands:"
    echo "    ./logs_all.sh --help"
    echo "    ./cleanup_all.sh --help"
    echo ""
}

# Function untuk show service list
show_services() {
    echo "📋 Available Services:"
    echo "====================="
    echo ""
    echo "🏥 Posyandu+ Services:"
    echo "  auth-service, posyandu-service, balita-service, ibu-hamil-service"
    echo "  imunisasi-service, kb-service, vitamin-service, rujukan-service"
    echo "  laporan-service, api-gateway, frontend"
    echo ""
    echo "🏥 POS BINDU PTM Services:"
    echo "  participant-service, screening-service, examination-service"
    echo "  lab-service, risk-assessment-service, intervention-service"
    echo "  referral-service, reporting-service, api-gateway, posbindu-frontend"
    echo ""
}

# Function untuk show examples
show_examples() {
    echo "💡 Usage Examples:"
    echo "=================="
    echo ""
    echo "🚀 Start everything:"
    echo "  ./start_all.sh"
    echo ""
    echo "🛑 Stop everything:"
    echo "  ./stop_all.sh"
    echo ""
    echo "🔄 Restart everything:"
    echo "  ./restart_all.sh"
    echo ""
    echo "📊 Check status:"
    echo "  ./status_all.sh"
    echo ""
    echo "🧪 Test everything:"
    echo "  ./test_all.sh"
    echo ""
    echo "📋 View logs:"
    echo "  ./logs_all.sh                    # All Posyandu+ logs"
    echo "  ./logs_all.sh auth-service       # Specific service logs"
    echo "  ./logs_all.sh participant-service # POS BINDU PTM service logs"
    echo ""
    echo "🧹 Cleanup:"
    echo "  ./cleanup_all.sh                 # Full cleanup"
    echo "  ./cleanup_all.sh --stop          # Stop only"
    echo "  ./cleanup_all.sh --images        # Clean images only"
    echo ""
}

# Main execution
main() {
    # Check for specific help type
    case "$1" in
        --services)
            show_services
            ;;
        --examples)
            show_examples
            ;;
        --help|-h)
            show_help
            ;;
        *)
            show_help
            ;;
    esac
}

# Run main function
main "$@"

echo "🆘 Help displayed! Use specific commands to get more information."
