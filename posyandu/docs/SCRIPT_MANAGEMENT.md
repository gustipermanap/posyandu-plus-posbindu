# 🎛️ Script Management - Posyandu+ & POS BINDU PTM

Dokumentasi lengkap untuk semua script management yang tersedia untuk mengelola aplikasi Posyandu+ dan POS BINDU PTM.

## 📋 Daftar Script

### 🚀 **Script Utama (Recommended)**

| Script | Deskripsi | Penggunaan |
|--------|-----------|------------|
| `./start_all.sh` | **Script utama untuk menjalankan semua services** | `./start_all.sh` |
| `./stop_all.sh` | Stop semua services | `./stop_all.sh` |
| `./restart_all.sh` | Restart semua services | `./restart_all.sh` |
| `./status_all.sh` | Check status semua services | `./status_all.sh` |
| `./test_all.sh` | Test semua services | `./test_all.sh` |

### 📋 **Script Logs & Monitoring**

| Script | Deskripsi | Penggunaan |
|--------|-----------|------------|
| `./logs_all.sh` | View logs semua services | `./logs_all.sh` |
| `./logs_all.sh [service]` | View logs service tertentu | `./logs_all.sh auth-service` |
| `./logs_all.sh --help` | Help untuk logs | `./logs_all.sh --help` |

### 🧹 **Script Cleanup**

| Script | Deskripsi | Penggunaan |
|--------|-----------|------------|
| `./cleanup_all.sh` | Full cleanup (stop + clean all) | `./cleanup_all.sh` |
| `./cleanup_all.sh --stop` | Stop semua services saja | `./cleanup_all.sh --stop` |
| `./cleanup_all.sh --images` | Clean images saja | `./cleanup_all.sh --images` |
| `./cleanup_all.sh --help` | Help untuk cleanup | `./cleanup_all.sh --help` |

### 🆘 **Script Help & Info**

| Script | Deskripsi | Penggunaan |
|--------|-----------|------------|
| `./help_all.sh` | Comprehensive help | `./help_all.sh` |
| `./help_all.sh --services` | Show available services | `./help_all.sh --services` |
| `./help_all.sh --examples` | Show usage examples | `./help_all.sh --examples` |
| `./scripts_info.sh` | Info semua script | `./scripts_info.sh` |
| `./manage.sh` | **Interactive management interface** | `./manage.sh` |

### 🔧 **Script Legacy (Masih Tersedia)**

| Script | Deskripsi | Penggunaan |
|--------|-----------|------------|
| `./setup_services.sh` | Setup Posyandu+ only | `./setup_services.sh` |
| `./test_api.sh` | Test Posyandu+ API only | `./test_api.sh` |
| `./run_microservices.sh` | Run Posyandu+ only | `./run_microservices.sh` |
| `./stop_microservices.sh` | Stop Posyandu+ only | `./stop_microservices.sh` |
| `./test_all_services.sh` | Test Posyandu+ only | `./test_all_services.sh` |

## 🚀 **Quick Start (1 Command)**

### **Mulai Semua Services**
```bash
./start_all.sh
```

**Ini adalah script utama yang kamu minta!** Script ini akan:
- ✅ Matikan port yang berjalan
- ✅ Stop containers yang ada
- ✅ Build dan start semua services
- ✅ Makemigrations dan migrate untuk semua services
- ✅ Collectstatic untuk semua services
- ✅ Test semua services
- ✅ Tampilkan status dan URL akses

### **Stop Semua Services**
```bash
./stop_all.sh
```

### **Restart Semua Services**
```bash
./restart_all.sh
```

### **Check Status**
```bash
./status_all.sh
```

### **Test Semua Services**
```bash
./test_all.sh
```

## 🎛️ **Interactive Mode**

### **Mode Interaktif**
```bash
./manage.sh
```

Mode interaktif akan menampilkan menu dengan pilihan:
1. start - Start all services
2. stop - Stop all services
3. restart - Restart all services
4. status - Check status of all services
5. test - Test all services
6. logs - View logs for all services
7. logs [service] - View logs for specific service
8. cleanup - Full cleanup (stop + clean all)
9. cleanup --stop - Stop all services only
10. cleanup --images - Clean images only
11. help - Show help
12. help --services - Show available services
13. help --examples - Show usage examples

### **Direct Command**
```bash
./manage.sh start                    # Start all services
./manage.sh stop                     # Stop all services
./manage.sh logs auth-service        # View auth-service logs
./manage.sh cleanup --images         # Clean images only
```

## 📋 **Logs & Monitoring**

### **View All Logs**
```bash
./logs_all.sh                       # All Posyandu+ logs
```

### **View Specific Service Logs**
```bash
./logs_all.sh auth-service          # Auth service logs
./logs_all.sh posyandu-service      # Posyandu service logs
./logs_all.sh balita-service        # Balita service logs
./logs_all.sh participant-service   # POS BINDU PTM participant logs
./logs_all.sh screening-service     # POS BINDU PTM screening logs
```

### **Available Services for Logs**
**Posyandu+ Services:**
- auth-service, posyandu-service, balita-service, ibu-hamil-service
- imunisasi-service, kb-service, vitamin-service, rujukan-service
- laporan-service, api-gateway, frontend

**POS BINDU PTM Services:**
- participant-service, screening-service, examination-service
- lab-service, risk-assessment-service, intervention-service
- referral-service, reporting-service, api-gateway, posbindu-frontend

## 🧹 **Cleanup Options**

### **Full Cleanup**
```bash
./cleanup_all.sh                    # Stop + clean all
```

### **Stop Only**
```bash
./cleanup_all.sh --stop             # Stop all services only
```

### **Clean Images Only**
```bash
./cleanup_all.sh --images           # Clean images only
```

### **Clean Containers Only**
```bash
./cleanup_all.sh --containers       # Clean containers only
```

### **Clean Volumes Only**
```bash
./cleanup_all.sh --volumes          # Clean volumes only
```

### **Clean Networks Only**
```bash
./cleanup_all.sh --networks         # Clean networks only
```

### **Clean System Only**
```bash
./cleanup_all.sh --system           # Clean system only
```

## 🆘 **Help & Information**

### **Comprehensive Help**
```bash
./help_all.sh                       # Show all help
./help_all.sh --services            # Show available services
./help_all.sh --examples            # Show usage examples
```

### **Script Information**
```bash
./scripts_info.sh                   # Show all script info
./scripts_info.sh --details         # Show detailed script info
./scripts_info.sh --examples        # Show usage examples
```

## 🌐 **Access URLs**

### **Posyandu+ Application**
- **Frontend**: http://localhost:3000
- **API**: http://localhost
- **Auth Service**: http://localhost:8001
- **Posyandu Service**: http://localhost:8002
- **Balita Service**: http://localhost:8003
- **Ibu Hamil Service**: http://localhost:8004
- **Imunisasi Service**: http://localhost:8005
- **KB Service**: http://localhost:8006
- **Vitamin Service**: http://localhost:8007
- **Rujukan Service**: http://localhost:8008
- **Laporan Service**: http://localhost:8009

### **POS BINDU PTM Application**
- **Frontend**: http://localhost:3001
- **API**: http://localhost:8080
- **Participant Service**: http://localhost:8005
- **Screening Service**: http://localhost:8006
- **Examination Service**: http://localhost:8007
- **Lab Service**: http://localhost:8008
- **Risk Assessment Service**: http://localhost:8009
- **Intervention Service**: http://localhost:8010
- **Referral Service**: http://localhost:8011
- **Reporting Service**: http://localhost:8012

## 🔑 **Demo Login**

- **Username**: admin
- **Password**: admin123

## 💡 **Usage Examples**

### **Daily Development Workflow**
```bash
# Start everything
./start_all.sh

# Check if everything is running
./status_all.sh

# View logs if needed
./logs_all.sh

# Test everything
./test_all.sh

# Stop when done
./stop_all.sh
```

### **Troubleshooting Workflow**
```bash
# Check what's running
./status_all.sh

# View logs for specific service
./logs_all.sh auth-service

# If services are not responding, restart
./restart_all.sh

# If still having issues, full cleanup and restart
./stop_all.sh
./cleanup_all.sh
./start_all.sh
```

### **Quick Commands**
```bash
# Quick start
./start_all.sh

# Quick stop
./stop_all.sh

# Quick restart
./restart_all.sh

# Quick status check
./status_all.sh

# Quick test
./test_all.sh
```

## 🔧 **Troubleshooting**

### **Port Conflicts**
```bash
# Stop all services
./stop_all.sh

# Start again
./start_all.sh
```

### **Services Not Responding**
```bash
# Check status
./status_all.sh

# View logs
./logs_all.sh

# Restart services
./restart_all.sh
```

### **Full Reset**
```bash
# Stop everything
./stop_all.sh

# Clean everything
./cleanup_all.sh

# Start fresh
./start_all.sh
```

### **Check Specific Service**
```bash
# Check logs
./logs_all.sh [service-name]

# Check status
./status_all.sh

# Test specific service
./test_all.sh
```

## 📊 **Service Ports**

### **Posyandu+ Services**
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

### **POS BINDU PTM Services**
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

## 🎯 **Best Practices**

### **Development**
1. Use `./start_all.sh` to start everything
2. Use `./status_all.sh` to check if everything is running
3. Use `./logs_all.sh` to monitor services
4. Use `./test_all.sh` to verify everything is working
5. Use `./stop_all.sh` when done

### **Production**
1. Use `./start_all.sh` to start services
2. Use `./status_all.sh` to monitor health
3. Use `./logs_all.sh` for debugging
4. Use `./restart_all.sh` for updates
5. Use `./cleanup_all.sh` for maintenance

### **Troubleshooting**
1. Always check `./status_all.sh` first
2. Use `./logs_all.sh` to identify issues
3. Try `./restart_all.sh` for quick fixes
4. Use `./cleanup_all.sh` for deep cleaning
5. Use `./start_all.sh` for fresh start

## 🚀 **Quick Reference**

| Command | Action |
|---------|--------|
| `./start_all.sh` | Start everything |
| `./stop_all.sh` | Stop everything |
| `./restart_all.sh` | Restart everything |
| `./status_all.sh` | Check status |
| `./test_all.sh` | Test everything |
| `./logs_all.sh` | View logs |
| `./cleanup_all.sh` | Clean up |
| `./help_all.sh` | Get help |
| `./manage.sh` | Interactive mode |

## 📚 **Documentation**

- **Main README**: [README.md](README.md)
- **Posyandu+ Documentation**: [posyandu/README.md](posyandu/README.md)
- **POS BINDU PTM Documentation**: [posbindu/README.md](posbindu/README.md)
- **API Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Complete Documentation**: [FINAL_COMPLETE_DOCUMENTATION.md](FINAL_COMPLETE_DOCUMENTATION.md)

## 🆘 **Support**

Jika mengalami masalah:
1. Jalankan `./help_all.sh` untuk bantuan
2. Jalankan `./status_all.sh` untuk check status
3. Jalankan `./logs_all.sh` untuk melihat logs
4. Jalankan `./cleanup_all.sh` untuk cleanup
5. Jalankan `./start_all.sh` untuk fresh start

---

**Script Management** - Membuat pengelolaan aplikasi Posyandu+ dan POS BINDU PTM menjadi mudah dan efisien! 🚀🇮🇩
