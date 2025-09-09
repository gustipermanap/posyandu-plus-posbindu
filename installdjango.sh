#!/bin/bash
# Membuat directory baru
echo "Masukkan nama directory baru (misalnya : dproject):"
read DIR

echo "Masukkan nama lingkungan virtual (misalnya: env): "
read ENV_NAME

# Menanyakan nama proyek Django kepada pengguna
echo "Masukkan nama proyek Django (misalnya: myproject): "
read PROJECT_NAME

# Menanyakan nama aplikasi Django kepada pengguna
echo "Masukkan nama aplikasi Django (misalnya: myapp): "
read APP_NAME

# Membuat Directory
echo "Membuat '$DIR'" 
mkdir $DIR
echo "Masuk ke '$DIR'"
cd $DIR

echo "membuat environtment"
python3 -m venv "$ENV_NAME"

echo "masuk kedalam environtment '$ENV_NAME'"
source "$ENV_NAME"/bin/activate

echo "menginstall paket django"
pip install /home/chloride/django-base/asgiref-3.8.1-py3-none-any.whl /home/chloride/django-base/Django-5.1-py3-none-any.whl /home/chloride/django-base/sqlparse-0.5.1-py3-none-any.whl 

echo "versi django"
python -m django --version

#-------------------------------------------------------------

# Membuat proyek Django baru dengan nama yang diberikan
echo "Membuat proyek Django dengan nama '$PROJECT_NAME'"
django-admin startproject "$PROJECT_NAME"

# Menampilkan pesan sukses
echo "Proyek Django '$PROJECT_NAME' berhasil dibuat!"

# Menampilkan struktur direktori proyek
echo "Struktur direktori proyek:"
ls -R "$PROJECT_NAME"

#-------------------------------------------------------------
cd "$PROJECT_NAME"
# Membuat aplikasi Django baru dengan nama yang diberikan
echo "Membuat aplikasi Django dengan nama '$APP_NAME'"
python manage.py startapp "$APP_NAME"

# Menampilkan pesan sukses
echo "Aplikasi Django '$APP_NAME' berhasil dibuat di proyek '$PROJECT_NAME'!"

# Menampilkan struktur direktori proyek dan aplikasi
echo "Struktur direktori proyek dan aplikasi:"
ls -R
