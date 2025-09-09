#!/bin/bash

# =============================================================================
# Backup and Restore All Applications (Posyandu + dan POS BINDU PTM)
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

# Function to backup Posyandu + databases
backup_posyandu_databases() {
    print_header "Backing up Posyandu + databases..."
    
    local backup_dir="backups/posyandu_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    local databases=(
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
    
    for db in "${databases[@]}"; do
        print_status "Backing up database: $db"
        docker-compose exec -T shared-database pg_dump -U postgres "$db" > "$backup_dir/${db}.sql"
        print_success "Backed up $db"
    done
    
    # Create archive
    print_status "Creating Posyandu + backup archive..."
    tar -czf "${backup_dir}.tar.gz" "$backup_dir"
    rm -rf "$backup_dir"
    
    print_success "Posyandu + database backup completed: ${backup_dir}.tar.gz"
    echo "${backup_dir}.tar.gz"
}

# Function to backup POS BINDU databases
backup_posbindu_databases() {
    print_header "Backing up POS BINDU PTM databases..."
    
    if [ ! -d "posbindu" ]; then
        print_warning "POS BINDU directory not found, skipping backup"
        return
    fi
    
    local backup_dir="backups/posbindu_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    local databases=(
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
    
    for db in "${databases[@]}"; do
        print_status "Backing up database: $db"
        docker-compose exec -T shared-database pg_dump -U postgres "$db" > "../$backup_dir/${db}.sql"
        print_success "Backed up $db"
    done
    
    cd ..
    
    # Create archive
    print_status "Creating POS BINDU backup archive..."
    tar -czf "${backup_dir}.tar.gz" "$backup_dir"
    rm -rf "$backup_dir"
    
    print_success "POS BINDU database backup completed: ${backup_dir}.tar.gz"
    echo "${backup_dir}.tar.gz"
}

# Function to backup all databases
backup_all_databases() {
    print_header "Backing up all databases..."
    
    local posyandu_backup=$(backup_posyandu_databases)
    local posbindu_backup=$(backup_posbindu_databases)
    
    # Create combined backup
    local combined_backup="backups/all_applications_$(date +%Y%m%d_%H%M%S).tar.gz"
    print_status "Creating combined backup archive..."
    
    tar -czf "$combined_backup" "$posyandu_backup" "$posbindu_backup" 2>/dev/null || true
    
    print_success "All databases backup completed: $combined_backup"
    echo "$combined_backup"
}

# Function to restore Posyandu + databases
restore_posyandu_databases() {
    local backup_file="$1"
    
    if [ -z "$backup_file" ]; then
        print_error "Backup file is required"
        return 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        print_error "Backup file not found: $backup_file"
        return 1
    fi
    
    print_header "Restoring Posyandu + databases from $backup_file..."
    
    # Extract backup
    local temp_dir=$(mktemp -d)
    tar -xzf "$backup_file" -C "$temp_dir"
    
    # Find the backup directory
    local backup_dir=$(find "$temp_dir" -type d -name "posyandu_*" | head -1)
    
    if [ -z "$backup_dir" ]; then
        print_error "Invalid backup file format"
        rm -rf "$temp_dir"
        return 1
    fi
    
    # Restore each database
    for sql_file in "$backup_dir"/*.sql; do
        if [ -f "$sql_file" ]; then
            local db_name=$(basename "$sql_file" .sql)
            print_status "Restoring database: $db_name"
            docker-compose exec -T shared-database psql -U postgres -d "$db_name" < "$sql_file"
            print_success "Restored $db_name"
        fi
    done
    
    # Cleanup
    rm -rf "$temp_dir"
    
    print_success "Posyandu + database restore completed"
}

# Function to restore POS BINDU databases
restore_posbindu_databases() {
    local backup_file="$1"
    
    if [ -z "$backup_file" ]; then
        print_error "Backup file is required"
        return 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        print_error "Backup file not found: $backup_file"
        return 1
    fi
    
    if [ ! -d "posbindu" ]; then
        print_error "POS BINDU directory not found"
        return 1
    fi
    
    print_header "Restoring POS BINDU PTM databases from $backup_file..."
    
    # Extract backup
    local temp_dir=$(mktemp -d)
    tar -xzf "$backup_file" -C "$temp_dir"
    
    # Find the backup directory
    local backup_dir=$(find "$temp_dir" -type d -name "posbindu_*" | head -1)
    
    if [ -z "$backup_dir" ]; then
        print_error "Invalid backup file format"
        rm -rf "$temp_dir"
        return 1
    fi
    
    cd posbindu
    
    # Restore each database
    for sql_file in "$backup_dir"/*.sql; do
        if [ -f "$sql_file" ]; then
            local db_name=$(basename "$sql_file" .sql)
            print_status "Restoring database: $db_name"
            docker-compose exec -T shared-database psql -U postgres -d "$db_name" < "$sql_file"
            print_success "Restored $db_name"
        fi
    done
    
    cd ..
    
    # Cleanup
    rm -rf "$temp_dir"
    
    print_success "POS BINDU database restore completed"
}

# Function to restore all databases
restore_all_databases() {
    local backup_file="$1"
    
    if [ -z "$backup_file" ]; then
        print_error "Backup file is required"
        return 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        print_error "Backup file not found: $backup_file"
        return 1
    fi
    
    print_header "Restoring all databases from $backup_file..."
    
    # Extract backup
    local temp_dir=$(mktemp -d)
    tar -xzf "$backup_file" -C "$temp_dir"
    
    # Find backup directories
    local posyandu_backup_dir=$(find "$temp_dir" -type d -name "posyandu_*" | head -1)
    local posbindu_backup_dir=$(find "$temp_dir" -type d -name "posbindu_*" | head -1)
    
    if [ -z "$posyandu_backup_dir" ] && [ -z "$posbindu_backup_dir" ]; then
        print_error "Invalid backup file format"
        rm -rf "$temp_dir"
        return 1
    fi
    
    # Restore Posyandu + databases
    if [ -n "$posyandu_backup_dir" ]; then
        for sql_file in "$posyandu_backup_dir"/*.sql; do
            if [ -f "$sql_file" ]; then
                local db_name=$(basename "$sql_file" .sql)
                print_status "Restoring database: $db_name"
                docker-compose exec -T shared-database psql -U postgres -d "$db_name" < "$sql_file"
                print_success "Restored $db_name"
            fi
        done
    fi
    
    # Restore POS BINDU databases
    if [ -n "$posbindu_backup_dir" ] && [ -d "posbindu" ]; then
        cd posbindu
        
        for sql_file in "$posbindu_backup_dir"/*.sql; do
            if [ -f "$sql_file" ]; then
                local db_name=$(basename "$sql_file" .sql)
                print_status "Restoring database: $db_name"
                docker-compose exec -T shared-database psql -U postgres -d "$db_name" < "$sql_file"
                print_success "Restored $db_name"
            fi
        done
        
        cd ..
    fi
    
    # Cleanup
    rm -rf "$temp_dir"
    
    print_success "All databases restore completed"
}

# Function to list available backups
list_backups() {
    print_header "Available Backups:"
    echo ""
    
    if [ -d "backups" ]; then
        ls -la backups/*.tar.gz 2>/dev/null || print_warning "No backup files found"
    else
        print_warning "Backups directory not found"
    fi
    echo ""
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --backup-all       Backup all databases"
    echo "  --backup-posyandu  Backup only Posyandu + databases"
    echo "  --backup-posbindu  Backup only POS BINDU PTM databases"
    echo "  --restore-all FILE Restore all databases from backup file"
    echo "  --restore-posyandu FILE Restore Posyandu + databases from backup file"
    echo "  --restore-posbindu FILE Restore POS BINDU databases from backup file"
    echo "  --list             List available backups"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --backup-all    Backup all databases"
    echo "  $0 --backup-posyandu  Backup only Posyandu + databases"
    echo "  $0 --restore-all backup.tar.gz  Restore all databases"
    echo "  $0 --list          List available backups"
}

# Main execution
main() {
    echo "============================================================================="
    echo "💾 Backup and Restore All Applications"
    echo "============================================================================="
    echo ""
    
    # Check prerequisites
    check_docker
    
    # Parse command line arguments
    BACKUP_ALL=false
    BACKUP_POSYANDU=false
    BACKUP_POSBINDU=false
    RESTORE_ALL=""
    RESTORE_POSYANDU=""
    RESTORE_POSBINDU=""
    LIST=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --backup-all)
                BACKUP_ALL=true
                shift
                ;;
            --backup-posyandu)
                BACKUP_POSYANDU=true
                shift
                ;;
            --backup-posbindu)
                BACKUP_POSBINDU=true
                shift
                ;;
            --restore-all)
                RESTORE_ALL="$2"
                shift 2
                ;;
            --restore-posyandu)
                RESTORE_POSYANDU="$2"
                shift 2
                ;;
            --restore-posbindu)
                RESTORE_POSBINDU="$2"
                shift 2
                ;;
            --list)
                LIST=true
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
    if [ "$LIST" = true ]; then
        list_backups
    elif [ "$BACKUP_ALL" = true ]; then
        backup_all_databases
    elif [ "$BACKUP_POSYANDU" = true ]; then
        backup_posyandu_databases
    elif [ "$BACKUP_POSBINDU" = true ]; then
        backup_posbindu_databases
    elif [ -n "$RESTORE_ALL" ]; then
        restore_all_databases "$RESTORE_ALL"
    elif [ -n "$RESTORE_POSYANDU" ]; then
        restore_posyandu_databases "$RESTORE_POSYANDU"
    elif [ -n "$RESTORE_POSBINDU" ]; then
        restore_posbindu_databases "$RESTORE_POSBINDU"
    else
        # Default: show help
        show_help
    fi
}

# Run main function
main "$@"