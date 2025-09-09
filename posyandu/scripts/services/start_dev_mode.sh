#!/bin/bash

# =============================================================================
# Start Development Mode (tanpa Docker)
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

# Function to check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    local python_version=$(python3 --version | cut -d' ' -f2)
    print_success "Python $python_version is installed"
}

# Function to check if virtual environment exists
check_virtual_env() {
    if [ ! -d "venv" ]; then
        print_warning "Virtual environment not found. Creating one..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    print_success "Virtual environment found"
}

# Function to activate virtual environment
activate_virtual_env() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Install common dependencies
    pip install -r requirements.txt 2>/dev/null || true
    
    # Install dependencies for each service
    services=(
        "posyandu/auth-service"
        "posyandu/posyandu-service"
        "posyandu/balita-service"
        "posyandu/ibu-hamil-service"
        "posyandu/imunisasi-service"
        "posyandu/kb-service"
        "posyandu/vitamin-service"
        "posyandu/rujukan-service"
        "posyandu/laporan-service"
    )
    
    for service in "${services[@]}"; do
        if [ -f "$service/requirements.txt" ]; then
            print_status "Installing dependencies for $service..."
            pip install -r "$service/requirements.txt"
        fi
    done
    
    print_success "Dependencies installed"
}

# Function to setup database
setup_database() {
    print_status "Setting up database..."
    
    # Check if PostgreSQL is running
    if ! pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
        print_warning "PostgreSQL is not running. Please start PostgreSQL first."
        print_status "You can start PostgreSQL with: sudo systemctl start postgresql"
        exit 1
    fi
    
    # Create databases
    databases=(
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
        print_status "Creating database: $db"
        createdb "$db" 2>/dev/null || print_warning "Database $db may already exist"
    done
    
    print_success "Database setup completed"
}

# Function to run migrations
run_migrations() {
    print_status "Running database migrations..."
    
    services=(
        "posyandu/auth-service"
        "posyandu/posyandu-service"
        "posyandu/balita-service"
        "posyandu/ibu-hamil-service"
        "posyandu/imunisasi-service"
        "posyandu/kb-service"
        "posyandu/vitamin-service"
        "posyandu/rujukan-service"
        "posyandu/laporan-service"
    )
    
    for service in "${services[@]}"; do
        if [ -d "$service" ]; then
            print_status "Running migrations for $service..."
            cd "$service"
            python manage.py makemigrations || true
            python manage.py migrate || true
            cd - >/dev/null
        fi
    done
    
    print_success "Migrations completed"
}

# Function to start services
start_services() {
    print_header "Starting services in development mode..."
    
    # Create log directory
    mkdir -p logs
    
    # Start services in background
    services=(
        "posyandu/auth-service:8001"
        "posyandu/posyandu-service:8002"
        "posyandu/balita-service:8003"
        "posyandu/ibu-hamil-service:8004"
        "posyandu/imunisasi-service:8005"
        "posyandu/kb-service:8006"
        "posyandu/vitamin-service:8007"
        "posyandu/rujukan-service:8008"
        "posyandu/laporan-service:8009"
    )
    
    for service_port in "${services[@]}"; do
        service=$(echo $service_port | cut -d: -f1)
        port=$(echo $service_port | cut -d: -f2)
        
        if [ -d "$service" ]; then
            print_status "Starting $service on port $port..."
            cd "$service"
            nohup python manage.py runserver 0.0.0.0:$port > "../../logs/${service##*/}.log" 2>&1 &
            cd - >/dev/null
            sleep 2
        fi
    done
    
    print_success "Services started in development mode"
}

# Function to start frontend
start_frontend() {
    print_status "Starting frontend..."
    
    if [ -d "posyandu/posyandu-frontend" ]; then
        cd posyandu/posyandu-frontend
        
        # Check if node_modules exists
        if [ ! -d "node_modules" ]; then
            print_status "Installing frontend dependencies..."
            npm install
        fi
        
        # Start frontend
        print_status "Starting React frontend on port 3000..."
        nohup npm start > "../../logs/frontend.log" 2>&1 &
        cd - >/dev/null
        
        print_success "Frontend started"
    else
        print_warning "Frontend directory not found"
    fi
}

# Function to show service status
show_service_status() {
    print_header "Service Status:"
    echo ""
    
    services=(
        "auth-service:8001"
        "posyandu-service:8002"
        "balita-service:8003"
        "ibu-hamil-service:8004"
        "imunisasi-service:8005"
        "kb-service:8006"
        "vitamin-service:8007"
        "rujukan-service:8008"
        "laporan-service:8009"
        "frontend:3000"
    )
    
    for service_port in "${services[@]}"; do
        service=$(echo $service_port | cut -d: -f1)
        port=$(echo $service_port | cut -d: -f2)
        
        if curl -s http://localhost:$port/ >/dev/null 2>&1; then
            print_success "$service is running on port $port"
        else
            print_warning "$service is not accessible on port $port"
        fi
    done
    echo ""
}

# Function to show access information
show_access_info() {
    echo ""
    echo "============================================================================="
    echo "🚀 Development Mode Started Successfully!"
    echo "============================================================================="
    echo ""
    echo "🌐 Access URLs:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Auth Service: http://localhost:8001"
    echo "  - Posyandu Service: http://localhost:8002"
    echo "  - Balita Service: http://localhost:8003"
    echo "  - Ibu Hamil Service: http://localhost:8004"
    echo "  - Imunisasi Service: http://localhost:8005"
    echo "  - KB Service: http://localhost:8006"
    echo "  - Vitamin Service: http://localhost:8007"
    echo "  - Rujukan Service: http://localhost:8008"
    echo "  - Laporan Service: http://localhost:8009"
    echo ""
    echo "📊 Useful Commands:"
    echo "  - View logs: tail -f logs/<service-name>.log"
    echo "  - Stop services: pkill -f 'python manage.py runserver'"
    echo "  - Stop frontend: pkill -f 'npm start'"
    echo "  - Check status: ./scripts/services/start_dev_mode.sh --status"
    echo ""
    echo "🔑 Login Credentials:"
    echo "  - Username: admin"
    echo "  - Password: admin123"
    echo ""
    echo "============================================================================="
}

# Function to stop services
stop_services() {
    print_header "Stopping development services..."
    
    # Stop Django services
    pkill -f 'python manage.py runserver' || true
    
    # Stop frontend
    pkill -f 'npm start' || true
    
    print_success "Development services stopped"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --start            Start all services in development mode"
    echo "  --stop             Stop all development services"
    echo "  --status           Show service status"
    echo "  --setup            Setup development environment"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --start         Start all services"
    echo "  $0 --stop          Stop all services"
    echo "  $0 --status        Show service status"
    echo "  $0 --setup         Setup development environment"
}

# Main execution
main() {
    echo "============================================================================="
    echo "🛠️ Starting Posyandu + Microservices in Development Mode"
    echo "============================================================================="
    echo ""
    
    # Parse command line arguments
    START=false
    STOP=false
    STATUS=false
    SETUP=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --start)
                START=true
                shift
                ;;
            --stop)
                STOP=true
                shift
                ;;
            --status)
                STATUS=true
                shift
                ;;
            --setup)
                SETUP=true
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
    if [ "$STOP" = true ]; then
        stop_services
    elif [ "$STATUS" = true ]; then
        show_service_status
    elif [ "$SETUP" = true ]; then
        check_python
        check_virtual_env
        activate_virtual_env
        install_dependencies
        setup_database
        run_migrations
        print_success "Development environment setup completed!"
    elif [ "$START" = true ]; then
        check_python
        check_virtual_env
        activate_virtual_env
        setup_database
        run_migrations
        start_services
        start_frontend
        show_service_status
        show_access_info
        print_success "Development mode started successfully!"
    else
        # Default: setup and start
        check_python
        check_virtual_env
        activate_virtual_env
        install_dependencies
        setup_database
        run_migrations
        start_services
        start_frontend
        show_service_status
        show_access_info
        print_success "Development mode started successfully!"
    fi
}

# Run main function
main "$@"
