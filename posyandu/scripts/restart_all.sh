#!/bin/bash

# Script untuk restart semua services Posyandu+ dan POS BINDU PTM

echo "🔄 Restarting All Services - Posyandu+ & POS BINDU PTM"
echo "===================================================="

# Function untuk restart services
restart_services() {
    echo "🔄 Restarting services..."
    
    # Restart Posyandu+ services
    echo "  - Restarting Posyandu+ services..."
    docker-compose restart
    
    # Restart POS BINDU PTM services
    echo "  - Restarting POS BINDU PTM services..."
    cd posbindu
    docker-compose restart
    cd ..
    
    echo "✅ All services restarted"
}

# Function untuk show status
show_status() {
    echo ""
    echo "🔄 All Services Restarted Successfully!"
    echo "======================================"
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
    echo "  Stop all: ./stop_all.sh"
    echo "  Start fresh: ./start_all.sh"
    echo "  View logs: docker-compose logs -f"
    echo ""
}

# Main execution
main() {
    # Restart services
    restart_services
    
    # Show status
    show_status
}

# Run main function
main

echo "🔄 All done! Services are restarted."
