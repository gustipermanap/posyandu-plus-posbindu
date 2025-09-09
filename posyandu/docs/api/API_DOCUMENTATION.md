# API Documentation - Posyandu Microservices

## Overview

Aplikasi Posyandu + menggunakan arsitektur microservices dengan 5 service utama:

1. **Auth Service** (Port 8001) - Autentikasi dan manajemen user
2. **Posyandu Service** (Port 8002) - Data posyandu dan peserta
3. **Balita Service** (Port 8003) - Pemeriksaan balita, imunisasi, vitamin
4. **Ibu Hamil Service** (Port 8004) - Pemeriksaan ibu hamil, suplemen, nifas
5. **Imunisasi Service** (Port 8005) - Jadwal dan pencatatan imunisasi

## Base URLs

- **API Gateway**: `http://localhost:80`
- **Frontend**: `http://localhost:3000`

## Authentication

Semua endpoint memerlukan authentication token. Dapatkan token dengan:

```bash
curl -X POST http://localhost:80/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

## Service Endpoints

### 1. Auth Service (`/api/auth/`)

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

#### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "kader1",
  "email": "kader1@posyandu.com",
  "password": "password123",
  "first_name": "Kader",
  "last_name": "Posyandu"
}
```

#### Profile
```http
GET /api/auth/profile/
Authorization: Bearer <token>
```

### 2. Posyandu Service (`/api/posyandu/`)

#### List Posyandu
```http
GET /api/posyandu/
```

#### Create Posyandu
```http
POST /api/posyandu/
Content-Type: application/json

{
  "nama": "Posyandu Melati",
  "alamat": "Jl. Melati No. 1",
  "rt": "01",
  "rw": "01",
  "desa": "Desa Melati",
  "kecamatan": "Kecamatan Melati",
  "kabupaten": "Kabupaten Melati",
  "nama_koordinator": "Siti Aminah",
  "no_hp_koordinator": "08123456789",
  "jadwal_posyandu": "Setiap hari Selasa minggu ke-2"
}
```

### 3. Balita Service (`/api/balita/`)

#### Pemeriksaan Balita

##### List Pemeriksaan
```http
GET /api/balita/pemeriksaan/
```

##### Create Pemeriksaan
```http
POST /api/balita/pemeriksaan/
Content-Type: application/json

{
  "visit_id": 1,
  "balita_id": 1,
  "posyandu_id": 1,
  "tanggal_pemeriksaan": "2024-01-15",
  "berat_badan": 12.5,
  "tinggi_badan": 85.0,
  "lingkar_kepala": 45.0,
  "lingkar_lengan": 15.0,
  "motorik_kasar": "sesuai",
  "motorik_halus": "sesuai",
  "bicara": "sesuai",
  "sosial": "sesuai",
  "catatan_perkembangan": "Perkembangan normal",
  "rekomendasi": "Lanjutkan stimulasi",
  "created_by": 1
}
```

##### Statistics
```http
GET /api/balita/pemeriksaan/statistics/
```

##### By Balita
```http
GET /api/balita/pemeriksaan/by_balita/?balita_id=1
```

#### Imunisasi Balita

##### List Imunisasi
```http
GET /api/balita/imunisasi/
```

##### Create Imunisasi
```http
POST /api/balita/imunisasi/
Content-Type: application/json

{
  "balita_id": 1,
  "posyandu_id": 1,
  "jenis_imunisasi": "bcg",
  "tanggal_imunisasi": "2024-01-15",
  "usia_saat_imunisasi": 2,
  "status": "diberikan",
  "lokasi_imunisasi": "posyandu",
  "petugas_imunisasi": "Dr. Siti",
  "catatan": "Imunisasi berjalan lancar",
  "created_by": 1
}
```

##### Statistics
```http
GET /api/balita/imunisasi/statistics/
```

#### Vitamin Balita

##### List Vitamin
```http
GET /api/balita/vitamin/
```

##### Create Vitamin
```http
POST /api/balita/vitamin/
Content-Type: application/json

{
  "balita_id": 1,
  "posyandu_id": 1,
  "jenis_vitamin": "vitamin_a",
  "tanggal_pemberian": "2024-01-15",
  "dosis": "100.000 IU",
  "status": "diberikan",
  "petugas_pemberian": "Kader Posyandu",
  "catatan": "Vitamin A diberikan",
  "created_by": 1
}
```

### 4. Ibu Hamil Service (`/api/ibu-hamil/`)

#### Pemeriksaan Ibu Hamil

##### List Pemeriksaan
```http
GET /api/ibu-hamil/pemeriksaan/
```

##### Create Pemeriksaan
```http
POST /api/ibu-hamil/pemeriksaan/
Content-Type: application/json

{
  "visit_id": 1,
  "ibu_hamil_id": 1,
  "posyandu_id": 1,
  "tanggal_pemeriksaan": "2024-01-15",
  "usia_kehamilan_minggu": 28,
  "tekanan_darah_sistol": 120,
  "tekanan_darah_diastol": 80,
  "nadi": 80,
  "tinggi_fundus": 28.0,
  "lingkar_lengan_atas": 25.0,
  "gerakan_janin": true,
  "hb": 12.0,
  "protein_urine": "negatif",
  "gula_darah": 90.0,
  "keluhan": "Tidak ada",
  "created_by": 1
}
```

##### Statistics
```http
GET /api/ibu-hamil/pemeriksaan/statistics/
```

#### Suplemen Ibu Hamil

##### List Suplemen
```http
GET /api/ibu-hamil/suplemen/
```

##### Create Suplemen
```http
POST /api/ibu-hamil/suplemen/
Content-Type: application/json

{
  "ibu_hamil_id": 1,
  "posyandu_id": 1,
  "jenis_suplemen": "fe_tablet",
  "tanggal_pemberian": "2024-01-15",
  "dosis": "1 tablet per hari",
  "jumlah": 30,
  "status": "diberikan",
  "petugas_pemberian": "Kader Posyandu",
  "catatan": "Fe tablet diberikan",
  "created_by": 1
}
```

### 5. Imunisasi Service (`/api/imunisasi/`)

#### Jadwal Imunisasi

##### List Jadwal
```http
GET /api/imunisasi/jadwal/
```

##### By Usia
```http
GET /api/imunisasi/jadwal/by_usia/?usia_bulan=12
```

#### Pencatatan Imunisasi

##### List Pencatatan
```http
GET /api/imunisasi/pencatatan/
```

##### Create Pencatatan
```http
POST /api/imunisasi/pencatatan/
Content-Type: application/json

{
  "balita_id": 1,
  "posyandu_id": 1,
  "jenis_imunisasi": "bcg",
  "tanggal_pemberian": "2024-01-15",
  "usia_saat_imunisasi_bulan": 2,
  "status": "diberikan",
  "lokasi_pemberian": "posyandu",
  "petugas_pemberian": "Dr. Siti",
  "batch_vaksin": "BCG2024001",
  "tanggal_kedaluwarsa": "2025-01-15",
  "created_by": 1
}
```

##### Statistics
```http
GET /api/imunisasi/pencatatan/statistics/
```

#### Reminder Imunisasi

##### List Reminder
```http
GET /api/imunisasi/reminder/
```

##### By Balita
```http
GET /api/imunisasi/reminder/by_balita/?balita_id=1
```

##### By Prioritas
```http
GET /api/imunisasi/reminder/by_prioritas/?prioritas=tinggi
```

#### Stok Vaksin

##### List Stok
```http
GET /api/imunisasi/stok/
```

##### Expiring Soon
```http
GET /api/imunisasi/stok/expiring_soon/
```

## Filtering and Search

### Query Parameters

- `search`: Pencarian teks
- `ordering`: Pengurutan (contoh: `-created_at`)
- `page`: Halaman (pagination)
- `page_size`: Jumlah item per halaman

### Filter Fields

Setiap endpoint memiliki filter fields yang berbeda:

- **Pemeriksaan Balita**: `balita_id`, `posyandu_id`, `status_gizi`, `tanggal_pemeriksaan`
- **Imunisasi Balita**: `balita_id`, `posyandu_id`, `jenis_imunisasi`, `status`, `tanggal_imunisasi`
- **Pemeriksaan Ibu Hamil**: `ibu_hamil_id`, `posyandu_id`, `risiko_tinggi`, `tanggal_pemeriksaan`

### Contoh Filtering

```bash
# Pemeriksaan balita dengan status gizi normal
GET /api/balita/pemeriksaan/?status_gizi=normal

# Imunisasi BCG yang sudah diberikan
GET /api/balita/imunisasi/?jenis_imunisasi=bcg&status=diberikan

# Pemeriksaan ibu hamil dengan risiko tinggi
GET /api/ibu-hamil/pemeriksaan/?risiko_tinggi=true

# Pencarian dengan teks
GET /api/balita/pemeriksaan/?search=normal

# Pengurutan
GET /api/balita/pemeriksaan/?ordering=-tanggal_pemeriksaan
```

## Error Handling

### Error Response Format

```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

### Common HTTP Status Codes

- `200 OK`: Request berhasil
- `201 Created`: Resource berhasil dibuat
- `400 Bad Request`: Request tidak valid
- `401 Unauthorized`: Tidak terautentikasi
- `403 Forbidden`: Tidak memiliki akses
- `404 Not Found`: Resource tidak ditemukan
- `500 Internal Server Error`: Error server

## Testing

### Manual Testing

```bash
# Test health check
curl http://localhost:80/health

# Test API endpoints
./test_api.sh

# Setup dan test semua services
./setup_services.sh
```

### Automated Testing

```bash
# Test semua endpoints
curl -s http://localhost:80/api/balita/pemeriksaan/statistics/ | jq
curl -s http://localhost:80/api/ibu-hamil/pemeriksaan/statistics/ | jq
curl -s http://localhost:80/api/imunisasi/pencatatan/statistics/ | jq
```

## Development

### Running Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f [service-name]

# Stop services
docker-compose down
```

### Database Migrations

```bash
# Run migrations for specific service
docker-compose exec [service-name] python manage.py makemigrations
docker-compose exec [service-name] python manage.py migrate
```

### Creating Superuser

```bash
# Create superuser for auth service
docker-compose exec auth-service python manage.py createsuperuser
```

## Monitoring

### Health Checks

- **API Gateway**: `GET /health`
- **Auth Service**: `GET /api/auth/health/`
- **Services**: `GET /api/[service]/` (returns 200 if healthy)

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs -f posyandu-service
docker-compose logs -f balita-service
docker-compose logs -f ibu-hamil-service
docker-compose logs -f imunisasi-service
```

## Security

### Authentication

- Semua endpoint memerlukan authentication token
- Token diperoleh melalui login endpoint
- Token harus disertakan dalam header: `Authorization: Bearer <token>`

### CORS

- CORS diaktifkan untuk semua origins
- Headers yang diizinkan: `DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization`

### Database

- Setiap service memiliki database terpisah
- Koneksi database menggunakan environment variables
- Database credentials tidak hardcoded
