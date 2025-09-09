# POS BINDU PTM Frontend

Frontend React untuk aplikasi POS BINDU PTM (Pos Binaan Terpadu Penyakit Tidak Menular).

## 🚀 Fitur

- **Dashboard**: Statistik lengkap dan monitoring real-time
- **Manajemen Peserta**: Registrasi dan data peserta POS BINDU PTM
- **Skrining**: Kunjungan dan anamnesis peserta
- **Pemeriksaan Fisik**: Tanda vital dan antropometri
- **Laboratorium**: Hasil lab dan manajemen stok
- **Penilaian Risiko**: Skoring dan kategorisasi risiko PTM
- **Intervensi**: Edukasi, konseling, dan monitoring
- **Rujukan**: Manajemen rujukan ke fasilitas kesehatan
- **Laporan**: Laporan harian, mingguan, bulanan, dan tahunan

## 🛠️ Teknologi

- **React 18**: Frontend framework
- **React Router**: Routing
- **Axios**: HTTP client
- **CSS3**: Styling dengan responsive design

## 📦 Instalasi

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm start
   ```

3. **Build for Production**
   ```bash
   npm run build
   ```

## 🔧 Konfigurasi

### Environment Variables

```bash
# API Base URL
REACT_APP_API_URL=http://localhost:8080

# Service URLs
REACT_APP_PARTICIPANT_SERVICE_URL=http://localhost:8005
REACT_APP_SCREENING_SERVICE_URL=http://localhost:8006
REACT_APP_EXAMINATION_SERVICE_URL=http://localhost:8007
REACT_APP_LAB_SERVICE_URL=http://localhost:8008
REACT_APP_RISK_ASSESSMENT_SERVICE_URL=http://localhost:8009
REACT_APP_INTERVENTION_SERVICE_URL=http://localhost:8010
REACT_APP_REFERRAL_SERVICE_URL=http://localhost:8011
REACT_APP_REPORTING_SERVICE_URL=http://localhost:8012
```

## 📱 Komponen

### Pages
- **Dashboard**: Halaman utama dengan statistik
- **ParticipantList**: Daftar peserta POS BINDU PTM
- **ScreeningList**: Data skrining dan anamnesis
- **ExaminationList**: Pemeriksaan fisik dan antropometri
- **LabList**: Hasil laboratorium dan stok
- **RiskAssessmentList**: Penilaian risiko PTM
- **InterventionList**: Intervensi kesehatan
- **ReferralList**: Manajemen rujukan
- **ReportList**: Laporan dan statistik

### Components
- **LoginPage**: Halaman login
- **Dashboard**: Dashboard utama
- **ParticipantList**: Daftar peserta
- **ScreeningList**: Daftar skrining
- **ExaminationList**: Daftar pemeriksaan
- **LabList**: Daftar laboratorium
- **RiskAssessmentList**: Daftar penilaian risiko
- **InterventionList**: Daftar intervensi
- **ReferralList**: Daftar rujukan
- **ReportList**: Daftar laporan

### Hooks
- **useAuth**: Authentication management

## 🎨 Styling

- **CSS Modules**: Scoped styling
- **Responsive Design**: Mobile-first approach
- **Modern UI**: Clean dan user-friendly interface
- **Color Scheme**: Professional healthcare theme

## 🔐 Authentication

- **Login**: Username/password authentication
- **Session Management**: LocalStorage-based
- **Role-based Access**: Admin dan user roles
- **Protected Routes**: Route protection

## 📊 Data Management

- **API Integration**: RESTful API calls
- **State Management**: React hooks
- **Error Handling**: Comprehensive error handling
- **Loading States**: Loading indicators

## 🚀 Deployment

### Docker

```bash
# Build image
docker build -t posbindu-frontend .

# Run container
docker run -p 3000:3000 posbindu-frontend
```

### Production Build

```bash
# Build for production
npm run build

# Serve static files
npx serve -s build
```

## 📱 Responsive Design

- **Mobile**: Optimized for mobile devices
- **Tablet**: Tablet-friendly layout
- **Desktop**: Full desktop experience
- **Breakpoints**: 768px, 1024px, 1200px

## 🔧 Development

### Scripts

```bash
# Start development server
npm start

# Run tests
npm test

# Build for production
npm run build

# Eject (not recommended)
npm run eject
```

### Code Structure

```
src/
├── components/          # React components
│   ├── Dashboard.js
│   ├── ParticipantList.js
│   ├── ScreeningList.js
│   ├── ExaminationList.js
│   ├── LabList.js
│   ├── RiskAssessmentList.js
│   ├── InterventionList.js
│   ├── ReferralList.js
│   ├── ReportList.js
│   └── LoginPage.js
├── hooks/              # Custom hooks
│   └── useAuth.js
├── utils/              # Utility functions
├── App.js              # Main app component
├── App.css             # App styles
├── index.js            # Entry point
└── index.css           # Global styles
```

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Check if backend services are running
   - Verify API URLs in configuration

2. **Build Errors**
   - Clear node_modules and reinstall
   - Check for syntax errors

3. **Styling Issues**
   - Verify CSS file imports
   - Check for conflicting styles

## 📞 Support

- **Documentation**: [POS BINDU PTM Docs](POSBINDU_DOCUMENTATION.md)
- **API Documentation**: [API Docs](API_DOCUMENTATION.md)
- **Issues**: GitHub Issues

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🎯 Status

Frontend POS BINDU PTM sudah **lengkap dan siap digunakan** dengan:

- ✅ **9 Halaman** lengkap dengan fitur
- ✅ **Responsive Design** untuk semua device
- ✅ **Authentication** system
- ✅ **API Integration** dengan semua services
- ✅ **Modern UI/UX** design
- ✅ **Error Handling** yang comprehensive

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/gustipermanap/posyanduplus.git
cd posyanduplus/posbindu/posbindu-frontend

# Install dependencies
npm install

# Start development server
npm start

# Access application
# http://localhost:3000
```

## 🔑 Demo Login

- **Username**: admin
- **Password**: admin123

---

**POS BINDU PTM Frontend** - Membantu deteksi dini dan pencegahan PTM di masyarakat! 🇮🇩
