# Posyandu + Microservices

Aplikasi microservices lengkap untuk manajemen Posyandu dengan fokus pada kesehatan ibu dan anak.

## 🎯 Overview

**Posyandu +** adalah aplikasi microservices yang fokus pada pelayanan kesehatan ibu dan anak di Posyandu. Aplikasi ini mengintegrasikan semua aspek pelayanan Posyandu mulai dari registrasi peserta, pemeriksaan balita, imunisasi, KB, vitamin & PMT, hingga rujukan dan laporan.

## 🏗️ Arsitektur

### Services (9 Microservices + Frontend)

1. **Auth Service** (Port 8001) - Autentikasi & otorisasi
2. **Posyandu Service** (Port 8002) - Data Posyandu
3. **Balita Service** (Port 8003) - Data Balita
4. **Ibu Hamil Service** (Port 8004) - Data Ibu Hamil
5. **Imunisasi Service** (Port 8005) - Data Imunisasi
6. **KB Service** (Port 8006) - KB & Kesehatan Reproduksi
7. **Vitamin Service** (Port 8007) - Vitamin & PMT
8. **Rujukan Service** (Port 8008) - Manajemen Rujukan
9. **Laporan Service** (Port 8009) - Laporan & Statistik
10. **Frontend** (Port 3000) - React.js application

### Infrastructure

- **API Gateway**: Nginx (Port 80)
- **Database**: PostgreSQL (Port 5432)
- **Containerization**: Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/gustipermanap/posyanduplus.git
   cd posyanduplus
   ```

2. **Start Services**
   ```bash
   ./setup_services.sh
   ```

3. **Access Application**
   - Frontend: http://localhost:3000
   - API: http://localhost
   - Login: admin/admin123

## 📱 Fitur Utama

- **Dashboard**: Statistik lengkap dan monitoring
- **Manajemen Balita**: Registrasi dan data balita
- **Ibu Hamil**: Pemeriksaan dan monitoring ibu hamil
- **Imunisasi**: Jadwal dan pencatatan imunisasi
- **KB & Kesehatan Reproduksi**: Manajemen KB dan konseling
- **Vitamin & PMT**: Distribusi vitamin dan PMT
- **Rujukan**: Manajemen rujukan ke fasilitas kesehatan
- **Laporan**: Laporan harian, mingguan, bulanan

## 🛠️ Development

### Project Structure

```
posyandu/
├── auth-service/            # Authentication service
├── posyandu-service/        # Core Posyandu service
├── balita-service/          # Balita management
├── ibu-hamil-service/       # Ibu hamil management
├── imunisasi-service/       # Imunisasi management
├── kb-service/              # KB & Kesehatan Reproduksi
├── vitamin-service/         # Vitamin & PMT
├── rujukan-service/         # Rujukan management
├── laporan-service/         # Laporan & statistik
└── api-gateway/             # API Gateway
```

### Commands

```bash
# Setup dan start semua services
./setup_services.sh

# Test semua services
./test_api.sh

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart
```

## 📊 Service Ports

- Auth Service: 8001
- Posyandu Service: 8002
- Balita Service: 8003
- Ibu Hamil Service: 8004
- Imunisasi Service: 8005
- KB Service: 8006
- Vitamin Service: 8007
- Rujukan Service: 8008
- Laporan Service: 8009
- API Gateway: 80
- Frontend: 3000
- Database: 5432

## 🔧 API Endpoints

### Total: 80+ Endpoints

- **Auth**: `/api/auth/`
- **Posyandu**: `/api/posyandu/`
- **Balita**: `/api/balita/`
- **Ibu Hamil**: `/api/ibu-hamil/`
- **Imunisasi**: `/api/imunisasi/`
- **KB**: `/api/kb/`
- **Vitamin**: `/api/vitamin/`
- **Rujukan**: `/api/rujukan/`
- **Laporan**: `/api/laporan/`

## 🔐 Authentication

- **Login**: admin/admin123
- **JWT Token**: Token-based authentication
- **Role-based Access**: Admin dan user roles

## 🚀 Deployment

### Production

```bash
# Set production environment
export DEBUG=False
export SECRET_KEY=your-secret-key
export DB_PASSWORD=secure-password

# Deploy
docker-compose up -d
```

### Scaling

- **Horizontal Scaling**: Tambah instance service
- **Database**: PostgreSQL cluster
- **Load Balancer**: Nginx atau HAProxy
- **Monitoring**: Prometheus + Grafana

## 🎯 Status

Aplikasi **Posyandu +** sudah **lengkap dan siap digunakan** dengan:

- ✅ **9 Microservices** yang berfungsi penuh
- ✅ **Frontend React** yang responsive
- ✅ **API Gateway** dengan routing lengkap
- ✅ **Database** terpisah per service
- ✅ **Dokumentasi** lengkap
- ✅ **Docker** containerization

## 📞 Support

- **Documentation**: [FINAL_COMPLETE_DOCUMENTATION.md](../FINAL_COMPLETE_DOCUMENTATION.md)
- **Issues**: GitHub Issues
- **Contact**: support@posyandu.com

## 📄 License

MIT License - lihat [LICENSE](LICENSE) file untuk detail.

## 🎉 Acknowledgments

- Django REST Framework
- React.js
- PostgreSQL
- Docker
- Nginx
- Tim pengembang Posyandu +

---

**Posyandu +** - Membantu kesehatan ibu dan anak di Posyandu! 🇮🇩

## 🔑 Demo Login

- **Username**: admin
- **Password**: admin123

## 🚀 Quick Commands

```bash
# Start all services
./setup_services.sh

# Test all services
./test_api.sh

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📊 Key Features

- **Manajemen Balita**: Registrasi, pemeriksaan, dan monitoring balita
- **Ibu Hamil**: Pemeriksaan dan monitoring ibu hamil
- **Imunisasi**: Jadwal dan pencatatan imunisasi lengkap
- **KB & Kesehatan Reproduksi**: Manajemen KB dan konseling
- **Vitamin & PMT**: Distribusi vitamin dan PMT terstruktur
- **Rujukan**: Manajemen rujukan terintegrasi
- **Laporan**: Dashboard real-time dan export berbagai format

Aplikasi ini siap digunakan untuk manajemen Posyandu yang modern dan efisien! 🇮🇩