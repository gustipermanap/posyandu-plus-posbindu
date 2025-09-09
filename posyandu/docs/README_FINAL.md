# Posyandu + - Aplikasi Microservices untuk Posyandu

## 🎯 Overview

Aplikasi **Posyandu +** adalah sistem microservices yang dirancang khusus untuk kebutuhan Posyandu (Pos Pelayanan Terpadu) dengan fokus pada **ibu & anak**. Aplikasi ini mengintegrasikan semua aspek pelayanan Posyandu mulai dari registrasi peserta, pemeriksaan balita, imunisasi, hingga laporan.

## 🏗️ Arsitektur Microservices

### Services

1. **Auth Service** (Port 8001)
   - Autentikasi dan manajemen user
   - JWT token authentication
   - User profiles dan roles

2. **Posyandu Service** (Port 8002)
   - Data posyandu dan lokasi
   - Data balita, ibu hamil, WUS
   - Master data peserta

3. **Balita Service** (Port 8003)
   - Pemeriksaan balita (antropometri, perkembangan)
   - Imunisasi balita
   - Vitamin dan PMT

4. **Ibu Hamil Service** (Port 8004)
   - Pemeriksaan ibu hamil
   - Suplemen (Fe tablet, kalsium)
   - Data nifas dan bayi baru lahir

5. **Imunisasi Service** (Port 8005)
   - Jadwal imunisasi berdasarkan usia
   - Pencatatan imunisasi
   - Reminder imunisasi
   - Stok vaksin

### Infrastructure

- **API Gateway**: Nginx (Port 80)
- **Database**: PostgreSQL (Port 5432)
- **Frontend**: React (Port 3000)
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

2. **Setup Environment**
   ```bash
   cp env.example .env
   # Edit .env sesuai kebutuhan
   ```

3. **Start Services**
   ```bash
   ./setup_services.sh
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - API: http://localhost:80
   - Admin: admin/admin123

## 📱 Fitur Utama

### Dashboard
- Statistik balita, ibu hamil, imunisasi, KB
- Status gizi balita (normal, kurang, lebih)
- Risiko ibu hamil (normal, tinggi)
- Jadwal posyandu bulan ini

### Balita (0-59 bulan)
- **Registrasi**: NIK, nama, tanggal lahir, orang tua
- **Pemeriksaan**: Antropometri (BB, TB, lingkar kepala, lengan)
- **Perkembangan**: Motorik kasar/halus, bicara, sosial
- **Imunisasi**: Jadwal lengkap sesuai usia
- **Vitamin**: Vitamin A, PMT

### Ibu Hamil
- **Registrasi**: Data kehamilan, HPHT, HPL
- **Pemeriksaan**: TD, nadi, tinggi fundus, Hb
- **Risiko**: Deteksi otomatis risiko tinggi
- **Suplemen**: Fe tablet, kalsium, asam folat
- **Nifas**: Pemeriksaan pasca persalinan

### Imunisasi
- **Jadwal**: Berdasarkan usia balita
- **Pencatatan**: Status pemberian, efek samping
- **Reminder**: Notifikasi imunisasi yang belum
- **Stok**: Manajemen stok vaksin

### KB & Kesehatan Reproduksi
- **WUS/PUS**: Data wanita usia subur
- **Metode KB**: Pil, suntik, IUD, implant, dll
- **Monitoring**: Efek samping, kontrol ulang

### Laporan
- Rekap bulanan posyandu
- Statistik cakupan imunisasi
- Data gizi balita
- Rujukan dan follow-up

## 🛠️ Development

### Project Structure

```
posyandu/
├── microservices/
│   ├── auth-service/
│   ├── posyandu-service/
│   ├── balita-service/
│   ├── ibu-hamil-service/
│   ├── imunisasi-service/
│   └── api-gateway/
├── posyandu/posyandu-frontend/
├── docker-compose.yml
├── setup_services.sh
├── test_api.sh
└── README_FINAL.md
```

### API Documentation

Lihat [API_DOCUMENTATION.md](API_DOCUMENTATION.md) untuk dokumentasi lengkap API endpoints.

### Testing

```bash
# Test semua API endpoints
./test_api.sh

# Test specific service
curl http://localhost:80/api/balita/pemeriksaan/statistics/
```

### Database Management

```bash
# Run migrations
docker-compose exec [service-name] python manage.py migrate

# Create superuser
docker-compose exec auth-service python manage.py createsuperuser
```

## 📊 Data Model

### Core Entities

- **Posyandu**: Lokasi dan informasi posyandu
- **Balita**: Data balita (0-59 bulan)
- **Ibu Hamil**: Data kehamilan dan pemeriksaan
- **WUS**: Wanita Usia Subur untuk KB
- **Pemeriksaan**: Data pemeriksaan balita dan ibu hamil
- **Imunisasi**: Jadwal dan pencatatan imunisasi
- **Suplemen**: Vitamin dan PMT

### Key Features

- **Status Gizi Otomatis**: Perhitungan berdasarkan BB/TB dan umur
- **Risiko Kehamilan**: Deteksi otomatis berdasarkan parameter klinis
- **Reminder Imunisasi**: Notifikasi berdasarkan jadwal
- **Audit Trail**: Pencatatan semua perubahan data
- **Role-based Access**: Akses berdasarkan peran user

## 🔧 Configuration

### Environment Variables

```bash
# Database
DB_NAME=posyandu_shared
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=shared-database
DB_PORT=5432

# Services
AUTH_SERVICE_URL=http://auth-service:8001
POSYANDU_SERVICE_URL=http://posyandu-service:8002
BALITA_SERVICE_URL=http://balita-service:8003
IBU_HAMIL_SERVICE_URL=http://ibu-hamil-service:8004
IMUNISASI_SERVICE_URL=http://imunisasi-service:8005
```

### Service Ports

- Auth Service: 8001
- Posyandu Service: 8002
- Balita Service: 8003
- Ibu Hamil Service: 8004
- Imunisasi Service: 8005
- API Gateway: 80
- Frontend: 3000
- Database: 5432

## 🚀 Deployment

### Production

1. **Environment Setup**
   ```bash
   # Set production environment variables
   export DEBUG=False
   export SECRET_KEY=your-secret-key
   export DB_PASSWORD=secure-password
   ```

2. **Build and Deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **SSL/HTTPS**
   - Configure Nginx with SSL certificates
   - Update CORS settings for production domain

### Scaling

- **Horizontal Scaling**: Tambah instance service
- **Database**: Gunakan PostgreSQL cluster
- **Load Balancer**: Nginx atau HAProxy
- **Monitoring**: Prometheus + Grafana

## 📈 Monitoring & Logs

### Health Checks

```bash
# Check service health
curl http://localhost:80/health
curl http://localhost:80/api/auth/health/
```

### Logs

```bash
# View all logs
docker-compose logs

# View specific service
docker-compose logs -f balita-service
```

### Metrics

- Response time per endpoint
- Database connection pool
- Memory dan CPU usage
- Error rates

## 🔒 Security

### Authentication
- JWT token-based authentication
- Token expiration dan refresh
- Role-based access control

### Data Protection
- Database encryption at rest
- HTTPS untuk production
- Input validation dan sanitization
- CORS configuration

### Backup
- Regular database backups
- Configuration backup
- Disaster recovery plan

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

### Development Guidelines

- Follow PEP 8 untuk Python
- Use TypeScript untuk frontend
- Write tests untuk new features
- Update documentation

## 📞 Support

### Documentation
- [API Documentation](API_DOCUMENTATION.md)
- [Service Architecture](POSYANDU_UPDATE.md)

### Issues
- GitHub Issues untuk bug reports
- Feature requests via GitHub Discussions

### Contact
- Email: support@posyandu.com
- Documentation: [docs.posyandu.com](https://docs.posyandu.com)

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

**Posyandu +** - Membantu Posyandu memberikan pelayanan terbaik untuk ibu dan anak Indonesia! 🇮🇩
