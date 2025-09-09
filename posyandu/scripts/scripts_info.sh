#!/bin/bash

# Script untuk menampilkan informasi semua script yang tersedia

echo "📋 Available Scripts - Posyandu+ & POS BINDU PTM"
echo "==============================================="

# Function untuk show script info
show_script_info() {
    echo "📋 Available Scripts:"
    echo "===================="
    echo ""
    echo "🎛️  Main Management Scripts:"
    echo "  ./manage.sh              # Main management script (interactive mode)"
    echo "  ./start_all.sh           # Start all services (Posyandu+ & POS BINDU PTM)"
    echo "  ./stop_all.sh            # Stop all services"
    echo "  ./restart_all.sh         # Restart all services"
    echo "  ./status_all.sh          # Check status of all services"
    echo "  ./test_all.sh            # Test all services"
    echo ""
    echo "📋 Logs & Monitoring:"
    echo "  ./logs_all.sh            # View logs for all Posyandu+ services"
    echo "  ./logs_all.sh [service]  # View logs for specific service"
    echo "  ./logs_all.sh --help     # Show logs help"
    echo ""
    echo "🧹 Cleanup:"
    echo "  ./cleanup_all.sh         # Full cleanup (stop + clean all)"
    echo "  ./cleanup_all.sh --stop  # Stop all services only"
    echo "  ./cleanup_all.sh --images # Clean images only"
    echo "  ./cleanup_all.sh --help  # Show cleanup help"
    echo ""
    echo "🆘 Help:"
    echo "  ./help_all.sh            # Show help"
    echo "  ./help_all.sh --services # Show available services"
    echo "  ./help_all.sh --examples # Show usage examples"
    echo ""
    echo "🔧 Legacy Scripts (still available):"
    echo "  ./setup_services.sh      # Setup Posyandu+ services only"
    echo "  ./test_api.sh            # Test Posyandu+ API only"
    echo "  ./run_microservices.sh   # Run Posyandu+ services only"
    echo "  ./stop_microservices.sh  # Stop Posyandu+ services only"
    echo "  ./test_all_services.sh   # Test Posyandu+ services only"
    echo ""
    echo "🌐 Quick Access:"
    echo "  📱 Posyandu+ Frontend: http://localhost:3000"
    echo "  🔗 Posyandu+ API: http://localhost"
    echo "  📱 POS BINDU PTM Frontend: http://localhost:3001"
    echo "  🔗 POS BINDU PTM API: http://localhost:8080"
    echo ""
    echo "🔑 Demo Login: admin / admin123"
    echo ""
    echo "💡 Recommended Usage:"
    echo "  For daily use: ./manage.sh"
    echo "  For quick start: ./start_all.sh"
    echo "  For troubleshooting: ./help_all.sh"
    echo ""
}

# Function untuk show script details
show_script_details() {
    echo "📋 Script Details:"
    echo "=================="
    echo ""
    echo "🎛️  Main Management Scripts:"
    echo "  ./manage.sh              # Interactive management interface"
    echo "    - Start/stop/restart all services"
    echo "    - View logs and status"
    echo "    - Run tests and cleanup"
    echo "    - Interactive mode with menu"
    echo ""
    echo "  ./start_all.sh           # Complete startup script"
    echo "    - Kill existing ports"
    echo "    - Stop existing containers"
    echo "    - Build and start all services"
    echo "    - Run migrations for all services"
    echo "    - Collect static files"
    echo "    - Test all services"
    echo ""
    echo "  ./stop_all.sh            # Complete shutdown script"
    echo "    - Kill existing ports"
    echo "    - Stop all containers"
    echo "    - Cleanup unused resources"
    echo ""
    echo "  ./restart_all.sh         # Restart all services"
    echo "    - Restart all containers"
    echo "    - Show status"
    echo ""
    echo "  ./status_all.sh          # Check service status"
    echo "    - Check container status"
    echo "    - Test API endpoints"
    echo "    - Show access URLs"
    echo ""
    echo "  ./test_all.sh            # Test all services"
    echo "    - Test all API endpoints"
    echo "    - Check service health"
    echo "    - Show summary"
    echo ""
    echo "📋 Logs & Monitoring:"
    echo "  ./logs_all.sh            # View logs"
    echo "    - View all Posyandu+ logs"
    echo "    - View specific service logs"
    echo "    - Help for log commands"
    echo ""
    echo "🧹 Cleanup:"
    echo "  ./cleanup_all.sh         # Cleanup system"
    echo "    - Stop all services"
    echo "    - Clean containers, images, volumes"
    echo "    - Clean networks and system"
    echo "    - Various cleanup options"
    echo ""
    echo "🆘 Help:"
    echo "  ./help_all.sh            # Comprehensive help"
    echo "    - Show all available commands"
    echo "    - Show service list"
    echo "    - Show usage examples"
    echo "    - Show troubleshooting tips"
    echo ""
}

# Function untuk show usage examples
show_usage_examples() {
    echo "💡 Usage Examples:"
    echo "=================="
    echo ""
    echo "🚀 Quick Start:"
    echo "  ./start_all.sh           # Start everything"
    echo "  ./status_all.sh          # Check if running"
    echo "  ./test_all.sh            # Test everything"
    echo ""
    echo "🛑 Quick Stop:"
    echo "  ./stop_all.sh            # Stop everything"
    echo "  ./cleanup_all.sh         # Clean up everything"
    echo ""
    echo "🔄 Quick Restart:"
    echo "  ./restart_all.sh         # Restart everything"
    echo ""
    echo "📋 View Logs:"
    echo "  ./logs_all.sh            # All Posyandu+ logs"
    echo "  ./logs_all.sh auth-service # Specific service logs"
    echo "  ./logs_all.sh participant-service # POS BINDU PTM logs"
    echo ""
    echo "🧹 Cleanup:"
    echo "  ./cleanup_all.sh         # Full cleanup"
    echo "  ./cleanup_all.sh --stop  # Stop only"
    echo "  ./cleanup_all.sh --images # Clean images only"
    echo ""
    echo "🆘 Get Help:"
    echo "  ./help_all.sh            # Show help"
    echo "  ./help_all.sh --services # Show services"
    echo "  ./help_all.sh --examples # Show examples"
    echo ""
    echo "🎛️  Interactive Mode:"
    echo "  ./manage.sh              # Start interactive mode"
    echo "  ./manage.sh start        # Direct command"
    echo "  ./manage.sh logs auth-service # Direct command with option"
    echo ""
}

# Main execution
main() {
    # Check for specific info type
    case "$1" in
        --details)
            show_script_details
            ;;
        --examples)
            show_usage_examples
            ;;
        --help|-h)
            show_script_info
            ;;
        *)
            show_script_info
            ;;
    esac
}

# Run main function
main "$@"

echo "📋 Script information displayed! Use specific options for more details."
