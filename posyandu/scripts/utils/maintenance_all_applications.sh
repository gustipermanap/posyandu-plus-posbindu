#!/bin/bash

# =============================================================================
# Maintenance All Applications (Posyandu + dan POS BINDU PTM)
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
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
    echo -e "${PURPLE}[HEADER]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to backup all databases
backup_all_databases() {
    print_header "Backing up all databases..."
    
    # Backup Posyandu + databases
    print_status "Backing up Posyandu + databases..."
    local posyandu_backup_dir="backups/posyandu_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$posyandu_backup_dir"
    
    local posyandu_databases=(
        "posyandu_auth"
        "posyandu_posyandu"
        "posyandu_balita"
        "posyandu_ibu_hamil"
        "posyandu_imunisasi"
        "posyandu_kb"
        "posyandu_vitamin"
        "posyandu_rujukan"
        "posyandu_laporan"
    )
    
    for db in "${posyandu_databases[@]}"; do
        print_status "Backing up database: $db"
        docker-compose exec -T shared-database pg_dump -U postgres "$db" > "$posyandu_backup_dir/${db}.sql"
        print_success "Backed up $db"
    done
    
    # Create Posyandu + archive
    print_status "Creating Posyandu + backup archive..."
    tar -czf "${posyandu_backup_dir}.tar.gz" "$posyandu_backup_dir"
    rm -rf "$posyandu_backup_dir"
    
    print_success "Posyandu + database backup completed: ${posyandu_backup_dir}.tar.gz"
    
    # Backup POS BINDU databases
    if [ -d "posbindu" ]; then
        print_status "Backing up POS BINDU PTM databases..."
        local posbindu_backup_dir="backups/posbindu_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$posbindu_backup_dir"
        
        local posbindu_databases=(
            "posbindu_participant"
            "posbindu_screening"
            "posbindu_examination"
            "posbindu_lab"
            "posbindu_risk_assessment"
            "posbindu_intervention"
            "posbindu_referral"
            "posbindu_reporting"
        )
        
        cd posbindu
        
        for db in "${posbindu_databases[@]}"; do
            print_status "Backing up database: $db"
            docker-compose exec -T shared-database pg_dump -U postgres "$db" > "../$posbindu_backup_dir/${db}.sql"
            print_success "Backed up $db"
        done
        
        cd ..
        
        # Create POS BINDU archive
        print_status "Creating POS BINDU backup archive..."
        tar -czf "${posbindu_backup_dir}.tar.gz" "$posbindu_backup_dir"
        rm -rf "$posbindu_backup_dir"
        
        print_success "POS BINDU database backup completed: ${posbindu_backup_dir}.tar.gz"
    else
        print_warning "POS BINDU directory not found, skipping backup"
    fi
    
    print_success "All databases backup completed"
}

# Function to clean up Docker resources
cleanup_docker() {
    print_header "Cleaning up Docker resources..."
    
    # Stop all services
    print_status "Stopping all services..."
    docker-compose down
    
    if [ -d "posbindu" ]; then
        cd posbindu
        docker-compose down
        cd ..
    fi
    
    # Remove unused containers
    print_status "Removing unused containers..."
    docker container prune -f
    
    # Remove unused images
    print_status "Removing unused images..."
    docker image prune -f
    
    # Remove unused volumes
    print_status "Removing unused volumes..."
    docker volume prune -f
    
    # Remove unused networks
    print_status "Removing unused networks..."
    docker network prune -f
    
    print_success "Docker cleanup completed"
}

# Function to clean up logs
cleanup_logs() {
    print_header "Cleaning up logs..."
    
    # Clean Docker logs
    print_status "Cleaning Docker logs..."
    docker-compose logs --tail=0 > /dev/null 2>&1 || true
    
    if [ -d "posbindu" ]; then
        cd posbindu
        docker-compose logs --tail=0 > /dev/null 2>&1 || true
        cd ..
    fi
    
    # Clean application logs
    if [ -d "logs" ]; then
        print_status "Cleaning application logs..."
        find logs -name "*.log" -mtime +7 -delete
        print_success "Application logs cleaned"
    fi
    
    print_success "Log cleanup completed"
}

# Function to update services
update_services() {
    print_header "Updating services..."
    
    # Update Posyandu + services
    print_status "Updating Posyandu + services..."
    docker-compose pull
    docker-compose build --no-cache
    docker-compose up -d
    
    # Update POS BINDU services
    if [ -d "posbindu" ]; then
        print_status "Updating POS BINDU PTM services..."
        cd posbindu
        docker-compose pull
        docker-compose build --no-cache
        docker-compose up -d
        cd ..
    fi
    
    print_success "Services updated successfully"
}

# Function to run migrations
run_migrations() {
    print_header "Running database migrations..."
    
    # Run migrations for Posyandu + services
    print_status "Running migrations for Posyandu + services..."
    local posyandu_services=(
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
    
    for service in "${posyandu_services[@]}"; do
        print_status "Running migrations for $service..."
        docker-compose exec -T "$service" python manage.py makemigrations || true
        docker-compose exec -T "$service" python manage.py migrate || true
    done
    
    # Run migrations for POS BINDU services
    if [ -d "posbindu" ]; then
        print_status "Running migrations for POS BINDU PTM services..."
        local posbindu_services=(
            "participant-service"
            "screening-service"
            "examination-service"
            "lab-service"
            "risk-assessment-service"
            "intervention-service"
            "referral-service"
            "reporting-service"
        )
        
        cd posbindu
        
        for service in "${posbindu_services[@]}"; do
            print_status "Running migrations for $service..."
            docker-compose exec -T "$service" python manage.py makemigrations || true
            docker-compose exec -T "$service" python manage.py migrate || true
        done
        
        cd ..
    fi
    
    print_success "All migrations completed"
}

# Function to check system health
check_system_health() {
    print_header "Checking system health..."
    
    # Check Docker
    if docker info >/dev/null 2>&1; then
        print_success "Docker is running"
    else
        print_error "Docker is not running"
    fi
    
    # Check disk space
    local disk_usage=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$disk_usage" -gt 80 ]; then
        print_warning "Disk usage is high: ${disk_usage}%"
    else
        print_success "Disk usage is normal: ${disk_usage}%"
    fi
    
    # Check memory
    local memory_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    if [ "$memory_usage" -gt 80 ]; then
        print_warning "Memory usage is high: ${memory_usage}%"
    else
        print_success "Memory usage is normal: ${memory_usage}%"
    fi
    
    # Check running services
    local posyandu_running=$(docker-compose ps --services --filter "status=running" | wc -l)
    local posyandu_total=12  # Total number of Posyandu + services
    
    if [ "$posyandu_running" -eq "$posyandu_total" ]; then
        print_success "All Posyandu + services are running ($posyandu_running/$posyandu_total)"
    else
        print_warning "Some Posyandu + services are not running ($posyandu_running/$posyandu_total)"
    fi
    
    # Check POS BINDU services
    if [ -d "posbindu" ]; then
        cd posbindu
        local posbindu_running=$(docker-compose ps --services --filter "status=running" | wc -l)
        local posbindu_total=11  # Total number of POS BINDU services
        
        if [ "$posbindu_running" -eq "$posbindu_total" ]; then
            print_success "All POS BINDU PTM services are running ($posbindu_running/$posbindu_total)"
        else
            print_warning "Some POS BINDU PTM services are not running ($posbindu_running/$posbindu_total)"
        fi
        
        cd ..
    else
        print_warning "POS BINDU directory not found"
    fi
}

# Function to show maintenance menu
show_maintenance_menu() {
    echo "============================================================================="
    echo "🔧 All Applications Maintenance"
    echo "============================================================================="
    echo ""
    echo "Select an option:"
    echo "1. Backup all databases"
    echo "2. Clean up Docker resources"
    echo "3. Clean up logs"
    echo "4. Update all services"
    echo "5. Run database migrations"
    echo "6. Check system health"
    echo "7. Full maintenance (backup + cleanup + migrations)"
    echo "8. Exit"
    echo ""
    read -p "Enter your choice (1-8): " choice
    
    case $choice in
        1)
            backup_all_databases
            ;;
        2)
            cleanup_docker
            ;;
        3)
            cleanup_logs
            ;;
        4)
            update_services
            ;;
        5)
            run_migrations
            ;;
        6)
            check_system_health
            ;;
        7)
            backup_all_databases
            cleanup_docker
            run_migrations
            ;;
        8)
            print_status "Exiting maintenance menu"
            exit 0
            ;;
        *)
            print_error "Invalid choice"
            ;;
    esac
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --backup           Backup all databases"
    echo "  --cleanup          Clean up Docker resources"
    echo "  --cleanup-logs     Clean up logs"
    echo "  --update           Update all services"
    echo "  --migrations       Run database migrations"
    echo "  --health           Check system health"
    echo "  --full             Full maintenance (backup + cleanup + migrations)"
    echo "  --menu             Show interactive menu"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --backup        Backup all databases"
    echo "  $0 --cleanup       Clean up Docker resources"
    echo "  $0 --full          Full maintenance"
    echo "  $0 --menu          Interactive menu"
}

# Main execution
main() {
    echo "============================================================================="
    echo "🔧 All Applications Maintenance (Posyandu + & POS BINDU PTM)"
    echo "============================================================================="
    echo ""
    
    # Check prerequisites
    check_docker
    
    # Parse command line arguments
    BACKUP=false
    CLEANUP=false
    CLEANUP_LOGS=false
    UPDATE=false
    MIGRATIONS=false
    HEALTH=false
    FULL=false
    MENU=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --backup)
                BACKUP=true
                shift
                ;;
            --cleanup)
                CLEANUP=true
                shift
                ;;
            --cleanup-logs)
                CLEANUP_LOGS=true
                shift
                ;;
            --update)
                UPDATE=true
                shift
                ;;
            --migrations)
                MIGRATIONS=true
                shift
                ;;
            --health)
                HEALTH=true
                shift
                ;;
            --full)
                FULL=true
                shift
                ;;
            --menu)
                MENU=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            -*)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                print_error "Unknown argument: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Execute based on options
    if [ "$MENU" = true ]; then
        show_maintenance_menu
    elif [ "$BACKUP" = true ]; then
        backup_all_databases
    elif [ "$CLEANUP" = true ]; then
        cleanup_docker
    elif [ "$CLEANUP_LOGS" = true ]; then
        cleanup_logs
    elif [ "$UPDATE" = true ]; then
        update_services
    elif [ "$MIGRATIONS" = true ]; then
        run_migrations
    elif [ "$HEALTH" = true ]; then
        check_system_health
    elif [ "$FULL" = true ]; then
        backup_all_databases
        cleanup_docker
        run_migrations
    else
        # Default: show interactive menu
        show_maintenance_menu
    fi
}

# Run main function
main "$@"