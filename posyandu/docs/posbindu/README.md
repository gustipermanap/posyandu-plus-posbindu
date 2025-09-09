# POS BINDU PTM - Pos Binaan Terpadu Penyakit Tidak Menular

Aplikasi microservices lengkap untuk deteksi dini dan pencegahan PTM di masyarakat.

## 🎯 Overview

**POS BINDU PTM** adalah aplikasi microservices yang fokus pada skrining, deteksi dini, dan manajemen faktor risiko PTM di masyarakat. Aplikasi ini mengintegrasikan semua aspek pelayanan POS BINDU PTM mulai dari registrasi peserta, skrining, pemeriksaan fisik, laboratorium, penilaian risiko, intervensi, rujukan, hingga laporan.

## 🏗️ Arsitektur

### Services (8 Microservices + Frontend)

1. **Participant Service** (Port 8005) - Data peserta
2. **Screening Service** (Port 8006) - Skrining dan anamnesis
3. **Examination Service** (Port 8007) - Pemeriksaan fisik
4. **Lab Service** (Port 8008) - Laboratorium
5. **Risk Assessment Service** (Port 8009) - Penilaian risiko
6. **Intervention Service** (Port 8010) - Intervensi kesehatan
7. **Referral Service** (Port 8011) - Manajemen rujukan
8. **Reporting Service** (Port 8012) - Laporan dan statistik
9. **Frontend** (Port 3001) - React.js application

### Infrastructure

- **API Gateway**: Nginx (Port 8080)
- **Database**: PostgreSQL (Port 5433)
- **Containerization**: Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/gustipermanap/posyanduplus.git
   cd posyanduplus/posbindu
   ```

2. **Start Services**
   ```bash
   ./setup_posbindu.sh
   ```

3. **Access Application**
   - Frontend: http://localhost:3001
   - API: http://localhost:8080
   - Login: admin/admin123

## 📱 Fitur Utama

- **Dashboard**: Statistik lengkap dan monitoring
- **Manajemen Peserta**: Registrasi dan data peserta
- **Skrining**: Kunjungan dan anamnesis
- **Pemeriksaan Fisik**: Tanda vital dan antropometri
- **Laboratorium**: Hasil lab dan stok management
- **Penilaian Risiko**: Skoring dan kategorisasi risiko
- **Intervensi**: Edukasi, konseling, dan monitoring
- **Rujukan**: Manajemen rujukan ke fasilitas kesehatan
- **Laporan**: Laporan harian, mingguan, bulanan

## 🛠️ Development

### Project Structure

```
posbindu/
├── participant-service/     # Data peserta
├── screening-service/       # Skrining dan anamnesis
├── examination-service/     # Pemeriksaan fisik
├── lab-service/            # Laboratorium
├── risk-assessment-service/ # Penilaian risiko
├── intervention-service/    # Intervensi kesehatan
├── referral-service/        # Manajemen rujukan
├── reporting-service/       # Laporan dan statistik
├── api-gateway/            # API Gateway
├── posbindu-frontend/      # Frontend React
├── docker-compose.yml      # Docker orchestration
├── setup_posbindu.sh       # Setup script
└── test_posbindu.sh        # Testing script
```

### Commands

```bash
# Setup dan start semua services
./setup_posbindu.sh

# Test semua services
./test_posbindu.sh

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart
```

## 📊 Service Ports

- Participant Service: 8005
- Screening Service: 8006
- Examination Service: 8007
- Lab Service: 8008
- Risk Assessment Service: 8009
- Intervention Service: 8010
- Referral Service: 8011
- Reporting Service: 8012
- API Gateway: 8080
- Frontend: 3001
- Database: 5433

## 🔧 API Endpoints

### Total: 80+ Endpoints

- **Participant**: `/api/participant/`
- **Screening**: `/api/screening/`
- **Examination**: `/api/examination/`
- **Lab**: `/api/lab/`
- **Risk Assessment**: `/api/risk-assessment/`
- **Intervention**: `/api/intervention/`
- **Referral**: `/api/referral/`
- **Reporting**: `/api/reporting/`

## 📚 Documentation

- [Dokumentasi Lengkap](POSBINDU_FINAL_DOCUMENTATION.md)
- [Dokumentasi API](POSBINDU_DOCUMENTATION.md)
- [Frontend Documentation](posbindu-frontend/README.md)

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

Aplikasi **POS BINDU PTM** sudah **lengkap dan siap digunakan** dengan:

- ✅ **8 Microservices** yang berfungsi penuh
- ✅ **Frontend React** yang responsive
- ✅ **API Gateway** dengan routing lengkap
- ✅ **Database** terpisah per service
- ✅ **Dokumentasi** lengkap
- ✅ **Docker** containerization

## 📞 Support

- **Documentation**: [POSBINDU_FINAL_DOCUMENTATION.md](POSBINDU_FINAL_DOCUMENTATION.md)
- **Issues**: GitHub Issues
- **Contact**: support@posbindu.com

## 📄 License

MIT License - lihat [LICENSE](LICENSE) file untuk detail.

## 🎉 Acknowledgments

- Django REST Framework
- React.js
- PostgreSQL
- Docker
- Nginx
- Tim pengembang POS BINDU PTM

---

**POS BINDU PTM** - Membantu deteksi dini dan pencegahan PTM di masyarakat! 🇮🇩

## 🔑 Demo Login

- **Username**: admin
- **Password**: admin123

## 🚀 Quick Commands

```bash
# Start all services
./setup_posbindu.sh

# Test all services
./test_posbindu.sh

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📊 Key Features

- **Skrining Faktor Risiko**: Deteksi dini faktor risiko PTM
- **Pemeriksaan Fisik**: Vital signs dan antropometri lengkap
- **Laboratorium**: Hasil lab terintegrasi dengan stok management
- **Penilaian Risiko**: Skoring dan kategorisasi otomatis
- **Intervensi**: Edukasi, konseling, dan monitoring terstruktur
- **Rujukan**: Manajemen rujukan terintegrasi
- **Laporan**: Dashboard real-time dan export berbagai format

Aplikasi ini siap digunakan untuk deteksi dini dan pencegahan PTM di masyarakat! 🇮🇩
