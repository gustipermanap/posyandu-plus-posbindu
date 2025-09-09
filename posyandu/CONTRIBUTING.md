## Panduan Kontribusi

Terima kasih ingin berkontribusi ke Posyandu+ monorepo! Dokumentasi ini menjelaskan cara setup, gaya commit, alur Git, dan standar PR.

## Setup Lingkungan
1. Fork repo ini lalu clone:
   ```bash
   git clone https://github.com/<username>/posyanduplus.git
   cd posyanduplus
   ```
2. Siapkan environment (opsional):
   ```bash
   cp env.example .env
   ```
3. Jalankan seluruh layanan:
   ```bash
   ./start_all.sh
   ```

## Alur Kerja Git
1. Buat branch dari `main`:
   ```bash
   git checkout -b feat/<deskripsi-singkat>
   ```
2. Commit kecil dan sering. Push branch Anda:
   ```bash
   git push -u origin feat/<deskripsi-singkat>
   ```
3. Buka Pull Request ke `main` dengan deskripsi perubahan, cara test, dan dampaknya.

## Gaya Commit (Conventional Commits)
Gunakan format berikut agar riwayat jelas dan otomatisasi mudah:

- `feat: ...` penambahan fitur
- `fix: ...` perbaikan bug
- `docs: ...` dokumentasi
- `chore: ...` housekeeping, pembaruan non-code
- `refactor: ...` perubahan internal tanpa fitur/bugfix
- `test: ...` menambah atau memperbaiki test

Contoh: `feat(auth): tambah endpoint refresh token`

## Standar Kode
- Backend: Django REST Framework, pastikan ada serializer, view, url, dan test minimal.
- Frontend: React, ikuti struktur yang ada, hindari side effect tidak perlu, gunakan `.env` untuk URL API.
- Jangan menambah dependency tanpa alasan kuat. Jelaskan di PR jika diperlukan.

## Menambah Layanan Baru
1. Buat folder service di `posyandu/` atau `posbindu/`.
2. Tambahkan `Dockerfile` dan `requirements.txt` (backend) atau `package.json` (frontend).
3. Daftarkan route di API Gateway (`nginx.conf`).
4. Tambahkan service ke `docker-compose.yml` beserta variabel lingkungan.
5. Update dokumentasi terkait (`docs/`, `README.md`).

## Testing Lokal
Gunakan skrip yang tersedia:
```bash
./test_all.sh
./scripts/manage.sh --logs <service-name>
```

## Review & Merging
- Semua PR memerlukan 1+ review.
- Pastikan CI (jika ada) dan test lokal hijau.
- Squash merge direkomendasikan agar riwayat bersih.

## Pelaporan Issue
Buat issue dengan template berikut:
- Ringkasan masalah
- Langkah reproduksi
- Perilaku yang diharapkan
- Log/error terkait

Terima kasih atas kontribusinya! 🎉


