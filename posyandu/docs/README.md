# Posyandu + & POS BINDU PTM Microservices

Aplikasi Posyandu + telah diubah menjadi arsitektur microservices dan terintegrasi dengan aplikasi POS BINDU PTM untuk deteksi dini dan pencegahan PTM di masyarakat.

## 🏗️ Arsitektur Microservices

### Posyandu + Services

1. **API Gateway** (Port 80) - Nginx reverse proxy
2. **Auth Service** (Port 8001) - Autentikasi dan otorisasi
3. **Posyandu Service** (Port 8002) - Data Posyandu
4. **Balita Service** (Port 8003) - Data Balita
5. **Ibu Hamil Service** (Port 8004) - Data Ibu Hamil
6. **Imunisasi Service** (Port 8005) - Data Imunisasi
7. **KB Service** (Port 8006) - KB & Kesehatan Reproduksi
8. **Vitamin Service** (Port 8007) - Vitamin & PMT
9. **Rujukan Service** (Port 8008) - Manajemen Rujukan
10. **Laporan Service** (Port 8009) - Laporan & Statistik
11. **Frontend** (Port 3000) - React application

### POS BINDU PTM Services

1. **Participant Service** (Port 8005) - Data peserta
2. **Screening Service** (Port 8006) - Skrining & anamnesis
3. **Examination Service** (Port 8007) - Pemeriksaan fisik
4. **Lab Service** (Port 8008) - Laboratorium
5. **Risk Assessment Service** (Port 8009) - Penilaian risiko
6. **Intervention Service** (Port 8010) - Intervensi kesehatan
7. **Referral Service** (Port 8011) - Manajemen rujukan
8. **Reporting Service** (Port 8012) - Laporan & statistik
9. **API Gateway** (Port 8080) - Nginx reverse proxy
10. **Frontend** (Port 3001) - React application

### Database

- **Posyandu + Database** (Port 5432):
  - `posyandu_auth` - Auth service
  - `posyandu_posyandu` - Posyandu service
  - `posyandu_balita` - Balita service
  - `posyandu_ibu_hamil` - Ibu Hamil service
  - `posyandu_imunisasi` - Imunisasi service
  - `posyandu_kb` - KB service
  - `posyandu_vitamin` - Vitamin service
  - `posyandu_rujukan` - Rujukan service
  - `posyandu_laporan` - Laporan service

- **POS BINDU PTM Database** (Port 5433):
  - `posbindu_participant` - Participant service
  - `posbindu_screening` - Screening service
  - `posbindu_examination` - Examination service
  - `posbindu_lab` - Lab service
  - `posbindu_risk_assessment` - Risk Assessment service
  - `posbindu_intervention` - Intervention service
  - `posbindu_referral` - Referral service
  - `posbindu_reporting` - Reporting service

## 🚀 Quick Start

### Prerequisites

- Docker
- Docker Compose

### Menjalankan Aplikasi

1. **Clone repository**
   ```bash
   git clone https://github.com/gustipermanap/posyanduplus.git
   cd posyanduplus
   ```

2. **Jalankan semua services**
   ```bash
   ./run_microservices.sh
   ```

3. **Akses aplikasi**
   - **Posyandu + Frontend**: http://localhost:3000
   - **Posyandu + API**: http://localhost
   - **POS BINDU PTM Frontend**: http://localhost:3001
   - **POS BINDU PTM API**: http://localhost:8080

### Testing API

```bash
./test_api.sh
```

### Menjalankan POS BINDU PTM

```bash
# Masuk ke direktori POS BINDU PTM
cd posbindu

# Setup dan start semua services
./setup_posbindu.sh

# Test semua services
./test_posbindu.sh
```

### Menghentikan Services

```bash
# Posyandu +
./stop_microservices.sh

# POS BINDU PTM
cd posbindu
docker-compose down
```

## 📁 Struktur Project

```
posyandu/
├── posyandu/                # Microservices Posyandu+
│   ├── auth-service/        # Authentication service
│   ├── posyandu-service/    # Core Posyandu service
│   ├── balita-service/      # Balita management
│   ├── ibu-hamil-service/   # Ibu hamil management
│   ├── imunisasi-service/   # Imunisasi management
│   ├── kb-service/          # KB & Kesehatan Reproduksi
│   ├── vitamin-service/     # Vitamin & PMT
│   ├── rujukan-service/     # Rujukan management
│   ├── laporan-service/     # Laporan & statistik
│   └── api-gateway/         # API Gateway
├── posbindu/                # Microservices Posbindu PTM
│   ├── participant-service/ # Data peserta
│   ├── screening-service/   # Skrining & anamnesis
│   ├── examination-service/ # Pemeriksaan fisik
│   ├── lab-service/         # Laboratorium
│   ├── risk-assessment-service/ # Penilaian risiko
│   ├── intervention-service/    # Intervensi kesehatan
│   ├── referral-service/        # Manajemen rujukan
│   ├── reporting-service/       # Laporan & statistik
│   ├── api-gateway/             # API Gateway
│   └── posbindu-frontend/       # Frontend Posbindu
├── posyandu/posyandu-frontend/ # Frontend Posyandu+
├── docker-compose.yml       # Docker orchestration
├── setup_services.sh        # Setup script
└── test_api.sh             # Testing script
```

## 🔧 Development

### Menambah Service Baru

1. Buat direktori service di `posyandu/` atau `posbindu/`
2. Buat Dockerfile dan requirements.txt
3. Update `nginx.conf` di api-gateway
4. Update `docker-compose.yml`
5. Update frontend untuk komunikasi dengan service baru

### Database Migration

```bash
# Masuk ke container service
docker-compose exec posyandu-service bash

# Jalankan migrasi
python manage.py makemigrations
python manage.py migrate
```

## 🔗 API Endpoints

### Auth Service
- `POST /api/auth/register/` - Registrasi user
- `GET /api/auth/profile/` - Profil user
- `POST /api/token/` - Login
- `POST /api/token/refresh/` - Refresh token

### Posyandu Service
- `GET /api/posyandu/` - List posyandu
- `POST /api/posyandu/` - Create posyandu
- `GET /api/posyandu/{id}/` - Detail posyandu
- `PUT /api/posyandu/{id}/` - Update posyandu
- `DELETE /api/posyandu/{id}/` - Delete posyandu

### Anak Service
- `GET /api/anak/` - List anak
- `POST /api/anak/` - Create anak
- `GET /api/anak/{id}/` - Detail anak
- `PUT /api/anak/{id}/` - Update anak
- `DELETE /api/anak/{id}/` - Delete anak

### Penimbangan Service
- `GET /api/penimbangan/` - List penimbangan
- `POST /api/penimbangan/` - Create penimbangan
- `GET /api/penimbangan/{id}/` - Detail penimbangan
- `PUT /api/penimbangan/{id}/` - Update penimbangan
- `DELETE /api/penimbangan/{id}/` - Delete penimbangan

## 🔮 Integrasi dengan Posbindu

Arsitektur microservices ini memungkinkan integrasi mudah dengan aplikasi Posbindu:

1. **Shared Auth Service** - SSO untuk kedua aplikasi
2. **Independent Services** - Setiap service dapat dikembangkan secara independen
3. **API Gateway** - Centralized routing dan load balancing
4. **Database Separation** - Data terpisah untuk setiap domain

Lihat `microservices/posbindu-integration.md` untuk detail implementasi.

## 🛠️ Technology Stack

- **Backend**: Django REST Framework
- **Frontend**: React
- **Database**: PostgreSQL
- **API Gateway**: Nginx
- **Containerization**: Docker & Docker Compose
- **Authentication**: JWT (Simple JWT)

## 🎯 Status Aplikasi

### Posyandu + (Lengkap)
- ✅ **9 Microservices** yang berfungsi penuh
- ✅ **Frontend React** yang responsive
- ✅ **API Gateway** dengan routing lengkap
- ✅ **Database** terpisah per service
- ✅ **Dokumentasi** lengkap
- ✅ **Docker** containerization

### POS BINDU PTM (Lengkap)
- ✅ **8 Microservices** yang berfungsi penuh
- ✅ **Frontend React** yang responsive
- ✅ **API Gateway** dengan routing lengkap
- ✅ **Database** terpisah per service
- ✅ **Dokumentasi** lengkap
- ✅ **Docker** containerization

## 🔑 Demo Login

### Posyandu +
- **Username**: admin
- **Password**: admin123

### POS BINDU PTM
- **Username**: admin
- **Password**: admin123

## 📚 Dokumentasi

- [Posyandu + Documentation](FINAL_COMPLETE_DOCUMENTATION.md)
- [POS BINDU PTM Documentation](posbindu/POSBINDU_FINAL_DOCUMENTATION.md)
- [API Documentation](API_DOCUMENTATION.md)

## 📝 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 Support

Untuk pertanyaan atau bantuan, silakan buat issue di repository ini.
