# 🚀 Quick Start - Posyandu+ & POS BINDU PTM

Panduan cepat untuk menjalankan aplikasi Posyandu+ dan POS BINDU PTM.

## ⚡ **1 Command untuk Semua**

```bash
./start_all.sh
```

**Script ini akan:**
- ✅ Matikan port yang berjalan
- ✅ Stop containers yang ada
- ✅ Build dan start semua services
- ✅ Makemigrations dan migrate
- ✅ Collectstatic
- ✅ Test semua services

## 🌐 **Access URLs**

- **Posyandu+ Frontend**: http://localhost:3000
- **Posyandu+ API**: http://localhost
- **POS BINDU PTM Frontend**: http://localhost:3001
- **POS BINDU PTM API**: http://localhost:8080

## 🔑 **Demo Login**

- **Username**: admin
- **Password**: admin123

## 🎛️ **Quick Commands**

| Command | Action |
|---------|--------|
| `./start_all.sh` | Start everything |
| `./stop_all.sh` | Stop everything |
| `./restart_all.sh` | Restart everything |
| `./status_all.sh` | Check status |
| `./test_all.sh` | Test everything |
| `./logs_all.sh` | View logs |
| `./cleanup_all.sh` | Clean up |
| `./manage.sh` | Interactive mode |

## 🆘 **Troubleshooting**

```bash
# Check status
./status_all.sh

# View logs
./logs_all.sh

# Restart if needed
./restart_all.sh

# Full reset
./stop_all.sh
./cleanup_all.sh
./start_all.sh
```

## 📚 **Documentation**

- **Script Management**: [SCRIPT_MANAGEMENT.md](SCRIPT_MANAGEMENT.md)
- **Main README**: [README.md](README.md)
- **Help**: `./help_all.sh`

---

**Quick Start** - Mulai aplikasi dalam 1 command! 🚀🇮🇩
