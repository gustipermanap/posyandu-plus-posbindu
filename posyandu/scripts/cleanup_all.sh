#!/bin/bash

# Script untuk cleanup semua services Posyandu+ dan POS BINDU PTM

echo "🧹 Cleanup All Services - Posyandu+ & POS BINDU PTM"
echo "================================================="

# Function untuk stop semua services
stop_all() {
    echo "🛑 Stopping all services..."
    
    # Stop Posyandu+ containers
    echo "  - Stopping Posyandu+ containers..."
    docker-compose down 2>/dev/null || true
    
    # Stop POS BINDU PTM containers
    echo "  - Stopping POS BINDU PTM containers..."
    cd posbindu
    docker-compose down 2>/dev/null || true
    cd ..
    
    echo "✅ All services stopped"
}

# Function untuk cleanup containers
cleanup_containers() {
    echo "🧹 Cleaning up containers..."
    
    # Remove stopped containers
    echo "  - Removing stopped containers..."
    docker container prune -f 2>/dev/null || true
    
    echo "✅ Containers cleaned up"
}

# Function untuk cleanup images
cleanup_images() {
    echo "🧹 Cleaning up images..."
    
    # Remove unused images
    echo "  - Removing unused images..."
    docker image prune -f 2>/dev/null || true
    
    # Remove dangling images
    echo "  - Removing dangling images..."
    docker image prune -a -f 2>/dev/null || true
    
    echo "✅ Images cleaned up"
}

# Function untuk cleanup volumes
cleanup_volumes() {
    echo "🧹 Cleaning up volumes..."
    
    # Remove unused volumes
    echo "  - Removing unused volumes..."
    docker volume prune -f 2>/dev/null || true
    
    echo "✅ Volumes cleaned up"
}

# Function untuk cleanup networks
cleanup_networks() {
    echo "🧹 Cleaning up networks..."
    
    # Remove unused networks
    echo "  - Removing unused networks..."
    docker network prune -f 2>/dev/null || true
    
    echo "✅ Networks cleaned up"
}

# Function untuk cleanup system
cleanup_system() {
    echo "🧹 Cleaning up system..."
    
    # Remove all unused data
    echo "  - Removing all unused data..."
    docker system prune -a -f 2>/dev/null || true
    
    echo "✅ System cleaned up"
}

# Function untuk show help
show_help() {
    echo "🧹 Cleanup All Services - Posyandu+ & POS BINDU PTM"
    echo "================================================="
    echo ""
    echo "Usage:"
    echo "  ./cleanup_all.sh                    # Full cleanup (stop + clean all)"
    echo "  ./cleanup_all.sh --stop             # Stop all services only"
    echo "  ./cleanup_all.sh --containers       # Clean containers only"
    echo "  ./cleanup_all.sh --images           # Clean images only"
    echo "  ./cleanup_all.sh --volumes          # Clean volumes only"
    echo "  ./cleanup_all.sh --networks         # Clean networks only"
    echo "  ./cleanup_all.sh --system           # Clean system only"
    echo "  ./cleanup_all.sh --help             # Show this help"
    echo ""
    echo "Examples:"
    echo "  ./cleanup_all.sh                    # Full cleanup"
    echo "  ./cleanup_all.sh --stop             # Stop services only"
    echo "  ./cleanup_all.sh --images           # Clean images only"
    echo ""
}

# Function untuk show status
show_status() {
    echo ""
    echo "📊 Cleanup Status:"
    echo "================="
    echo ""
    echo "🛠️ Management Commands:"
    echo "  Start all: ./start_all.sh"
    echo "  Stop all: ./stop_all.sh"
    echo "  Restart all: ./restart_all.sh"
    echo "  Check status: ./status_all.sh"
    echo "  View logs: ./logs_all.sh"
    echo "  Test all: ./test_all.sh"
    echo ""
}

# Main execution
main() {
    # Check for help flag
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_help
        return 0
    fi
    
    # Check for specific cleanup type
    case "$1" in
        --stop)
            stop_all
            ;;
        --containers)
            cleanup_containers
            ;;
        --images)
            cleanup_images
            ;;
        --volumes)
            cleanup_volumes
            ;;
        --networks)
            cleanup_networks
            ;;
        --system)
            cleanup_system
            ;;
        *)
            # Full cleanup
            stop_all
            cleanup_containers
            cleanup_images
            cleanup_volumes
            cleanup_networks
            cleanup_system
            ;;
    esac
    
    # Show status
    show_status
}

# Run main function
main "$@"
echo "🧹 Cleanup completed!"

