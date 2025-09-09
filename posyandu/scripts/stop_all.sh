#!/bin/bash

# Script untuk stop semua services Posyandu+ dan POS BINDU PTM

echo "🛑 Stopping All Services - Posyandu+ & POS BINDU PTM"
echo "=================================================="

# Function untuk matikan port yang berjalan
kill_ports() {
    echo "🛑 Killing existing ports..."
    
    # Matikan port yang mungkin berjalan
    fuser -k 80/tcp 2>/dev/null || true
    fuser -k 3000/tcp 2>/dev/null || true
    fuser -k 3001/tcp 2>/dev/null || true
    fuser -k 8001/tcp 2>/dev/null || true
    fuser -k 8002/tcp 2>/dev/null || true
    fuser -k 8003/tcp 2>/dev/null || true
    fuser -k 8004/tcp 2>/dev/null || true
    fuser -k 8005/tcp 2>/dev/null || true
    fuser -k 8006/tcp 2>/dev/null || true
    fuser -k 8007/tcp 2>/dev/null || true
    fuser -k 8008/tcp 2>/dev/null || true
    fuser -k 8009/tcp 2>/dev/null || true
    fuser -k 8010/tcp 2>/dev/null || true
    fuser -k 8011/tcp 2>/dev/null || true
    fuser -k 8012/tcp 2>/dev/null || true
    fuser -k 8080/tcp 2>/dev/null || true
    fuser -k 5432/tcp 2>/dev/null || true
    fuser -k 5433/tcp 2>/dev/null || true
    
    echo "✅ Ports killed"
}

# Function untuk stop containers
stop_containers() {
    echo "🛑 Stopping existing containers..."
    
    # Stop Posyandu+ containers
    echo "  - Stopping Posyandu+ containers..."
    docker compose down 2>/dev/null || true
    
    # Stop POS BINDU PTM containers
    echo "  - Stopping POS BINDU PTM containers..."
    cd posbindu
    docker compose down 2>/dev/null || true
    cd ..
    
    echo "✅ All containers stopped"
}

# Function untuk cleanup
cleanup() {
    echo "🧹 Cleaning up..."
    
    # Remove unused containers
    docker container prune -f 2>/dev/null || true
    
    # Remove unused images
    docker image prune -f 2>/dev/null || true
    
    # Remove unused volumes
    docker volume prune -f 2>/dev/null || true
    
    echo "✅ Cleanup completed"
}

# Function untuk show status
show_status() {
    echo ""
    echo "✅ All Services Stopped Successfully!"
    echo "===================================="
    echo ""
    echo "🛠️ To start services again:"
    echo "  ./start_all.sh"
    echo ""
    echo "📊 To check running containers:"
    echo "  docker ps"
    echo ""
}

# Main execution
main() {
    # Kill existing ports
    kill_ports
    
    # Stop existing containers
    stop_containers
    
    # Cleanup
    cleanup
    
    # Show status
    show_status
}

# Run main function
main

echo "🛑 All done! Services are stopped."
