#!/bin/bash

# Script lengkap untuk menjalankan semua services Posyandu+ dan POS BINDU PTM
# Termasuk matikan port, makemigrations, migrate, collectstatic

echo "🚀 Starting All Services - Posyandu+ & POS BINDU PTM"
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
    docker compose down 2>/dev/null || true
    
    # Stop POS BINDU PTM containers
    cd posbindu
    docker compose down 2>/dev/null || true
    cd ..
    
    echo "✅ Containers stopped"
}

# Function untuk start Posyandu+ services
start_posyandu() {
    echo "🏥 Starting Posyandu+ Services..."
    echo "================================="
    
    # Build and start Posyandu+ services
    docker compose up -d --build
    
    # Wait for services to be ready
    echo "⏳ Waiting for Posyandu+ services to be ready..."
    sleep 30
    
    # Run migrations for each service
    echo "📊 Running Posyandu+ migrations..."
    
    # Auth Service
    echo "  - Auth Service migrations..."
    docker compose exec -T auth-service python manage.py makemigrations
    docker compose exec -T auth-service python manage.py migrate
    
    # Posyandu Service
    echo "  - Posyandu Service migrations..."
    docker compose exec -T posyandu-service python manage.py makemigrations
    docker compose exec -T posyandu-service python manage.py migrate
    
    # Balita Service
    echo "  - Balita Service migrations..."
    docker compose exec -T balita-service python manage.py makemigrations
    docker compose exec -T balita-service python manage.py migrate
    
    # Ibu Hamil Service
    echo "  - Ibu Hamil Service migrations..."
    docker compose exec -T ibu-hamil-service python manage.py makemigrations
    docker compose exec -T ibu-hamil-service python manage.py migrate
    
    # Imunisasi Service
    echo "  - Imunisasi Service migrations..."
    docker compose exec -T imunisasi-service python manage.py makemigrations
    docker compose exec -T imunisasi-service python manage.py migrate
    
    # KB Service
    echo "  - KB Service migrations..."
    docker compose exec -T kb-service python manage.py makemigrations
    docker compose exec -T kb-service python manage.py migrate
    
    # Vitamin Service
    echo "  - Vitamin Service migrations..."
    docker compose exec -T vitamin-service python manage.py makemigrations
    docker compose exec -T vitamin-service python manage.py migrate
    
    # Rujukan Service
    echo "  - Rujukan Service migrations..."
    docker compose exec -T rujukan-service python manage.py makemigrations
    docker compose exec -T rujukan-service python manage.py migrate
    
    # Laporan Service
    echo "  - Laporan Service migrations..."
    docker compose exec -T laporan-service python manage.py makemigrations
    docker compose exec -T laporan-service python manage.py migrate
    
    # Collect static files
    echo "📁 Collecting static files..."
    docker compose exec -T auth-service python manage.py collectstatic --noinput
    docker compose exec -T posyandu-service python manage.py collectstatic --noinput
    docker compose exec -T balita-service python manage.py collectstatic --noinput
    docker compose exec -T ibu-hamil-service python manage.py collectstatic --noinput
    docker compose exec -T imunisasi-service python manage.py collectstatic --noinput
    docker compose exec -T kb-service python manage.py collectstatic --noinput
    docker compose exec -T vitamin-service python manage.py collectstatic --noinput
    docker compose exec -T rujukan-service python manage.py collectstatic --noinput
    docker compose exec -T laporan-service python manage.py collectstatic --noinput
    
    echo "✅ Posyandu+ services ready!"
}

# Function untuk start POS BINDU PTM services
start_posbindu() {
    echo "🏥 Starting POS BINDU PTM Services..."
    echo "===================================="
    
    # Build and start POS BINDU PTM services
    cd posbindu
    docker compose up -d --build
    
    # Wait for services to be ready
    echo "⏳ Waiting for POS BINDU PTM services to be ready..."
    sleep 30
    
    # Run migrations for each service
    echo "📊 Running POS BINDU PTM migrations..."
    
    # Participant Service
    echo "  - Participant Service migrations..."
    docker compose exec -T participant-service python manage.py makemigrations
    docker compose exec -T participant-service python manage.py migrate
    
    # Screening Service
    echo "  - Screening Service migrations..."
    docker compose exec -T screening-service python manage.py makemigrations
    docker compose exec -T screening-service python manage.py migrate
    
    # Examination Service
    echo "  - Examination Service migrations..."
    docker compose exec -T examination-service python manage.py makemigrations
    docker compose exec -T examination-service python manage.py migrate
    
    # Lab Service
    echo "  - Lab Service migrations..."
    docker compose exec -T lab-service python manage.py makemigrations
    docker compose exec -T lab-service python manage.py migrate
    
    # Risk Assessment Service
    echo "  - Risk Assessment Service migrations..."
    docker compose exec -T risk-assessment-service python manage.py makemigrations
    docker compose exec -T risk-assessment-service python manage.py migrate
    
    # Intervention Service
    echo "  - Intervention Service migrations..."
    docker compose exec -T intervention-service python manage.py makemigrations
    docker compose exec -T intervention-service python manage.py migrate
    
    # Referral Service
    echo "  - Referral Service migrations..."
    docker compose exec -T referral-service python manage.py makemigrations
    docker compose exec -T referral-service python manage.py migrate
    
    # Reporting Service
    echo "  - Reporting Service migrations..."
    docker compose exec -T reporting-service python manage.py makemigrations
    docker compose exec -T reporting-service python manage.py migrate
    
    # Collect static files
    echo "📁 Collecting static files..."
    docker compose exec -T participant-service python manage.py collectstatic --noinput
    docker compose exec -T screening-service python manage.py collectstatic --noinput
    docker compose exec -T examination-service python manage.py collectstatic --noinput
    docker compose exec -T lab-service python manage.py collectstatic --noinput
    docker compose exec -T risk-assessment-service python manage.py collectstatic --noinput
    docker compose exec -T intervention-service python manage.py collectstatic --noinput
    docker compose exec -T referral-service python manage.py collectstatic --noinput
    docker compose exec -T reporting-service python manage.py collectstatic --noinput
    
    echo "✅ POS BINDU PTM services ready!"
    cd ..
}

# Function untuk test services
test_services() {
    echo "🧪 Testing all services..."
    echo "========================="
    
    # Test Posyandu+ services
    echo "Testing Posyandu+ services..."
    ./test_api.sh
    
    # Test POS BINDU PTM services
    echo "Testing POS BINDU PTM services..."
    cd posbindu
    ./test_posbindu.sh
    cd ..
    
    echo "✅ All services tested!"
}

# Function untuk show status
show_status() {
    echo ""
    echo "🎉 All Services Started Successfully!"
    echo "====================================="
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
    echo "📊 Service Status:"
    echo "  Posyandu+ Services: 9 microservices + frontend"
    echo "  POS BINDU PTM Services: 8 microservices + frontend"
    echo ""
    echo "🛠️ Management Commands:"
    echo "  Stop all: docker compose down && cd posbindu && docker compose down && cd .."
    echo "  View logs: docker compose logs -f"
    echo "  Restart: ./start_all.sh"
    echo ""
}

# Main execution
main() {
    # Kill existing ports
    kill_ports
    
    # Stop existing containers
    stop_containers
    
    # Start Posyandu+ services
    start_posyandu
    
    # Start POS BINDU PTM services
    start_posbindu
    
    # Test all services
    test_services
    
    # Show status
    show_status
}

# Run main function
main

echo "🚀 All done! Services are running."
