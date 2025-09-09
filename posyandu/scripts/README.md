# 📁 Scripts Management untuk Posyandu + Microservices

Folder ini berisi semua script shell untuk mengelola dan menjalankan aplikasi Posyandu + Microservices dengan mudah.

## 🗂️ Struktur Folder

```
scripts/
├── manage.sh                 # Script utama untuk mengelola semua
├── docker/                   # Script untuk setup Docker
│   └── setup_docker.sh      # Setup Docker environment
├── services/                 # Script untuk mengelola services
│   ├── start_all_services.sh # Start semua services
│   ├── stop_all_services.sh  # Stop semua services
│   ├── start_service.sh      # Start service individual
│   └── restart_service.sh    # Restart service individual
├── utils/                    # Script utility
│   ├── monitor_services.sh   # Monitoring services
│   └── maintenance.sh        # Maintenance dan cleanup
└── README.md                # Dokumentasi ini
```

## 🚀 Quick Start

### 1. Setup Awal
```bash
# Setup Docker environment
./scripts/manage.sh --setup

# Atau menggunakan script langsung
./scripts/docker/setup_docker.sh
```

### 2. Menjalankan Services
```bash
# Start semua services
./scripts/manage.sh --start

# Atau menggunakan script langsung
./scripts/services/start_all_services.sh
```

### 3. Monitoring
```bash
# Lihat status services
./scripts/manage.sh --status

# Monitor real-time
./scripts/utils/monitor_services.sh --monitor
```

## 📋 Daftar Script

### 🎯 Script Utama
- **`manage.sh`** - Script utama dengan menu interaktif
  ```bash
  ./scripts/manage.sh                    # Menu interaktif
  ./scripts/manage.sh --start            # Start semua services
  ./scripts/manage.sh --status           # Lihat status
  ./scripts/manage.sh --logs auth-service # Lihat logs
  ```

### 🐳 Docker Setup
- **`docker/setup_docker.sh`** - Setup Docker environment
  ```bash
  ./scripts/docker/setup_docker.sh
  ```
  - Check Docker installation
  - Pull base images
  - Build custom images
  - Setup database
  - Run migrations
  - Create superuser

### 🔧 Service Management
- **`services/start_all_services.sh`** - Start semua services
  ```bash
  ./scripts/services/start_all_services.sh
  ./scripts/services/start_all_services.sh --no-migrations
  ./scripts/services/start_all_services.sh --quick
  ```

- **`services/stop_all_services.sh`** - Stop semua services
  ```bash
  ./scripts/services/stop_all_services.sh
  ./scripts/services/stop_all_services.sh --cleanup
  ./scripts/services/stop_all_services.sh auth-service
  ```

- **`services/start_service.sh`** - Start service individual
  ```bash
  ./scripts/services/start_service.sh auth-service
  ./scripts/services/start_service.sh balita-service --no-migrations
  ./scripts/services/start_service.sh frontend --no-deps
  ```

- **`services/restart_service.sh`** - Restart service individual
  ```bash
  ./scripts/services/restart_service.sh auth-service
  ./scripts/services/restart_service.sh balita-service --no-migrations
  ```

### 📊 Monitoring & Maintenance
- **`utils/monitor_services.sh`** - Monitoring services
  ```bash
  ./scripts/utils/monitor_services.sh --status        # Status overview
  ./scripts/utils/monitor_services.sh --monitor       # Real-time monitoring
  ./scripts/utils/monitor_services.sh --endpoints     # Health check
  ./scripts/utils/monitor_services.sh --resources     # System resources
  ./scripts/utils/monitor_services.sh auth-service    # Detailed info
  ```

- **`utils/maintenance.sh`** - Maintenance dan cleanup
  ```bash
  ./scripts/utils/maintenance.sh --backup             # Backup databases
  ./scripts/utils/maintenance.sh --restore backup.tar.gz # Restore backup
  ./scripts/utils/maintenance.sh --cleanup            # Cleanup Docker
  ./scripts/utils/maintenance.sh --migrations         # Run migrations
  ./scripts/utils/maintenance.sh --health             # System health
  ./scripts/utils/maintenance.sh --full               # Full maintenance
  ./scripts/utils/maintenance.sh --menu               # Interactive menu
  ```

## 🌐 Access URLs

Setelah services berjalan, Anda dapat mengakses:

- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost
- **Auth Service**: http://localhost:8001
- **Posyandu Service**: http://localhost:8002
- **Balita Service**: http://localhost:8003
- **Ibu Hamil Service**: http://localhost:8004
- **Imunisasi Service**: http://localhost:8005
- **KB Service**: http://localhost:8006
- **Vitamin Service**: http://localhost:8007
- **Rujukan Service**: http://localhost:8008
- **Laporan Service**: http://localhost:8009

## 🔑 Login Credentials

- **Username**: admin
- **Password**: admin123

## 📋 Available Services

| Service | Port | Description |
|---------|------|-------------|
| shared-database | 5432 | PostgreSQL database |
| auth-service | 8001 | Authentication service |
| posyandu-service | 8002 | Core Posyandu service |
| balita-service | 8003 | Balita management |
| ibu-hamil-service | 8004 | Ibu hamil management |
| imunisasi-service | 8005 | Imunisasi management |
| kb-service | 8006 | KB & Kesehatan Reproduksi |
| vitamin-service | 8007 | Vitamin & PMT |
| rujukan-service | 8008 | Rujukan management |
| laporan-service | 8009 | Laporan & statistik |
| api-gateway | 80 | Nginx reverse proxy |
| frontend | 3000 | React application |

## 🛠️ Development Workflow

### 1. Setup Awal
```bash
# Clone repository
git clone https://github.com/gustipermanap/posyandu-plus-posbindu.git
cd posyandu-plus-posbindu

# Setup Docker environment
./scripts/manage.sh --setup
```

### 2. Development
```bash
# Start semua services
./scripts/manage.sh --start

# Monitor services
./scripts/manage.sh --monitor

# Lihat logs service tertentu
./scripts/manage.sh --logs auth-service

# Access shell service
./scripts/manage.sh --shell auth-service
```

### 3. Maintenance
```bash
# Backup databases
./scripts/utils/maintenance.sh --backup

# Cleanup Docker resources
./scripts/utils/maintenance.sh --cleanup

# Run migrations
./scripts/utils/maintenance.sh --migrations
```

## 🔧 Troubleshooting

### Service Tidak Bisa Start
```bash
# Check Docker status
docker info

# Check service logs
./scripts/manage.sh --logs <service-name>

# Restart service
./scripts/services/restart_service.sh <service-name>
```

### Database Issues
```bash
# Run migrations
./scripts/utils/maintenance.sh --migrations

# Check database connection
./scripts/utils/monitor_services.sh --endpoints
```

### Resource Issues
```bash
# Check system resources
./scripts/utils/monitor_services.sh --resources

# Cleanup Docker resources
./scripts/utils/maintenance.sh --cleanup
```

## 📚 Tips & Best Practices

1. **Selalu gunakan script management** untuk operasi sehari-hari
2. **Backup database** secara berkala sebelum update
3. **Monitor resources** untuk menghindari masalah performa
4. **Gunakan real-time monitoring** saat development
5. **Check logs** jika ada masalah dengan service

## 🤝 Contributing

Jika Anda ingin menambah atau memperbaiki script:

1. Buat script di folder yang sesuai
2. Berikan permission executable: `chmod +x script.sh`
3. Update dokumentasi ini
4. Test script sebelum commit

## 📞 Support

Untuk pertanyaan atau masalah dengan script, silakan buat issue di repository ini.
