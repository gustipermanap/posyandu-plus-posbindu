#!/bin/bash

# =============================================================================
# Script: Posyandu+ Maintenance
# Description: Maintenance tasks untuk Posyandu+ services (backup, cleanup, migrations)
# Author: Posyandu+ Development Team
# Version: 1.0
# =============================================================================

set -e

# Colors untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function untuk print dengan warna
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${CYAN}=== $1 ===${NC}"
}

# Function untuk menampilkan help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --backup           Backup databases"
    echo "  --restore FILE     Restore from backup file"
    echo "  --cleanup          Cleanup Docker resources"
    echo "  --migrations       Run database migrations"
    echo "  --health           System health check"
    echo "  --full             Full maintenance (backup + cleanup + health)"
    echo "  --menu             Interactive menu"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --backup        # Backup databases"
    echo "  $0 --restore backup.tar.gz  # Restore from backup"
    echo "  $0 --cleanup       # Cleanup Docker resources"
    echo "  $0 --full          # Full maintenance"
}

# Function untuk backup databases
backup_databases() {
    print_header "Database Backup"
    
    # Create backup directory
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    print_status "Creating backup in: $BACKUP_DIR"
    
    # List of services with databases
    services=(
        "auth-service"
        "posyandu-service"
        "balita-service"
        "ibu-hamil-service"
        "imunisasi-service"
        "kb-service"
        "vitamin-service"
        "rujukan-service"
        "laporan-service"
    )
    
    for service in "${services[@]}"; do
        print_status "Backing up $service database..."
        
        # Create database dump
        if docker-compose exec -T "$service" python manage.py dumpdata > "$BACKUP_DIR/${service}_data.json" 2>/dev/null; then
            print_success "Backed up $service data"
        else
            print_warning "Failed to backup $service data"
        fi
    done
    
    # Create compressed archive
    print_status "Creating compressed archive..."
    tar -czf "${BACKUP_DIR}.tar.gz" -C "$(dirname "$BACKUP_DIR")" "$(basename "$BACKUP_DIR")"
    rm -rf "$BACKUP_DIR"
    
    print_success "Backup completed: ${BACKUP_DIR}.tar.gz"
}

# Function untuk restore databases
restore_databases() {
    local backup_file="$1"
    
    if [ -z "$backup_file" ]; then
        print_error "Backup file not specified"
        exit 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        print_error "Backup file not found: $backup_file"
        exit 1
    fi
    
    print_header "Database Restore"
    print_warning "This will overwrite existing data. Are you sure? (y/N)"
    read -r response
    
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_status "Restore cancelled"
        exit 0
    fi
    
    # Extract backup
    print_status "Extracting backup: $backup_file"
    BACKUP_DIR="backups/restore_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    tar -xzf "$backup_file" -C "$BACKUP_DIR" --strip-components=1
    
    # Restore data for each service
    services=(
        "auth-service"
        "posyandu-service"
        "balita-service"
        "ibu-hamil-service"
        "imunisasi-service"
        "kb-service"
        "vitamin-service"
        "rujukan-service"
        "laporan-service"
    )
    
    for service in "${services[@]}"; do
        local data_file="$BACKUP_DIR/${service}_data.json"
        
        if [ -f "$data_file" ]; then
            print_status "Restoring $service data..."
            
            if docker-compose exec -T "$service" python manage.py loaddata /dev/stdin < "$data_file" 2>/dev/null; then
                print_success "Restored $service data"
            else
                print_warning "Failed to restore $service data"
            fi
        else
            print_warning "No backup data found for $service"
        fi
    done
    
    # Cleanup
    rm -rf "$BACKUP_DIR"
    
    print_success "Restore completed"
}

# Function untuk cleanup Docker resources
cleanup_docker() {
    print_header "Docker Cleanup"
    
    print_status "Removing stopped containers..."
    docker container prune -f
    
    print_status "Removing unused images..."
    docker image prune -f
    
    print_status "Removing unused volumes..."
    docker volume prune -f
    
    print_status "Removing unused networks..."
    docker network prune -f
    
    print_status "System cleanup..."
    docker system prune -f
    
    print_success "Docker cleanup completed"
}

# Function untuk run migrations
run_migrations() {
    print_header "Database Migrations"
    
    # List of services that need migrations
    services=(
        "auth-service"
        "posyandu-service"
        "balita-service"
        "ibu-hamil-service"
        "imunisasi-service"
        "kb-service"
        "vitamin-service"
        "rujukan-service"
        "laporan-service"
    )
    
    for service in "${services[@]}"; do
        print_status "Running migrations for $service..."
        
        if docker-compose exec -T "$service" python manage.py migrate --noinput; then
            print_success "Migrations completed for $service"
        else
            print_warning "Failed to run migrations for $service"
        fi
    done
    
    print_success "All migrations completed"
}

# Function untuk system health check
system_health() {
    print_header "System Health Check"
    
    # Check Docker
    print_status "Checking Docker..."
    if docker info > /dev/null 2>&1; then
        print_success "Docker is running"
    else
        print_error "Docker is not running"
        return 1
    fi
    
    # Check services
    print_status "Checking services..."
    if [ -f "docker-compose.yml" ]; then
        docker-compose ps
    else
        print_error "docker-compose.yml not found"
        return 1
    fi
    
    # Check disk space
    print_status "Checking disk space..."
    df -h
    
    # Check memory
    print_status "Checking memory..."
    free -h
    
    # Check Docker resources
    print_status "Checking Docker resources..."
    docker system df
    
    print_success "Health check completed"
}

# Function untuk full maintenance
full_maintenance() {
    print_header "Full Maintenance"
    
    print_status "Starting full maintenance process..."
    
    # Backup
    backup_databases
    
    # Cleanup
    cleanup_docker
    
    # Health check
    system_health
    
    print_success "Full maintenance completed"
}

# Function untuk interactive menu
interactive_menu() {
    while true; do
        clear
        print_header "Posyandu+ Maintenance Menu"
        
        echo "1. Backup databases"
        echo "2. Restore from backup"
        echo "3. Run migrations"
        echo "4. Cleanup Docker resources"
        echo "5. System health check"
        echo "6. Full maintenance"
        echo "7. Exit"
        echo ""
        
        read -p "Select an option (1-7): " choice
        
        case $choice in
            1)
                backup_databases
                ;;
            2)
                read -p "Enter backup file path: " backup_file
                restore_databases "$backup_file"
                ;;
            3)
                run_migrations
                ;;
            4)
                cleanup_docker
                ;;
            5)
                system_health
                ;;
            6)
                full_maintenance
                ;;
            7)
                print_status "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid option. Please select 1-7."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Parse arguments
MODE="menu"

while [[ $# -gt 0 ]]; do
    case $1 in
        --backup)
            MODE="backup"
            shift
            ;;
        --restore)
            MODE="restore"
            RESTORE_FILE="$2"
            shift 2
            ;;
        --cleanup)
            MODE="cleanup"
            shift
            ;;
        --migrations)
            MODE="migrations"
            shift
            ;;
        --health)
            MODE="health"
            shift
            ;;
        --full)
            MODE="full"
            shift
            ;;
        --menu)
            MODE="menu"
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Execute based on mode
case $MODE in
    "backup")
        backup_databases
        ;;
    "restore")
        restore_databases "$RESTORE_FILE"
        ;;
    "cleanup")
        cleanup_docker
        ;;
    "migrations")
        run_migrations
        ;;
    "health")
        system_health
        ;;
    "full")
        full_maintenance
        ;;
    "menu")
        interactive_menu
        ;;
    *)
        interactive_menu
        ;;
esac
