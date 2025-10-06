# 🎓 COOP Prasetiya Mulya

Platform digital untuk mengelola program magang mahasiswa Universitas Prasetiya Mulya. Project ini dikembangkan sebagai UTS mata kuliah Web Application Development. Sistem ini menghubungkan mahasiswa, supervisor, dan tim administrasi COOP dalam satu platform terintegrasi.

## 📋 Fitur

* **Registrasi Mahasiswa** - Pendaftaran mandiri dengan email @student.prasetiyamulya.ac.id
* **Manajemen Lowongan** - Browse dan apply lowongan magang dari berbagai perusahaan
* **Laporan Bulanan** - Submit dan review laporan kemajuan magang
* **Evaluasi UTS/UAS** - Sistem evaluasi mahasiswa oleh supervisor dengan 24+ kriteria penilaian
* **Dashboard Interaktif** - Monitor status magang, aplikasi, dan progres secara real-time
* **Role-based Access** - Akses berbeda untuk Mahasiswa, Supervisor, dan Admin

## 💻 Teknologi yang Digunakan

* **Django 5.2.7** – Backend framework dengan Python
* **Bootstrap 5** – Responsive UI framework
* **SQLite** – Database management
* **Font Awesome 6** – Icon library
* **jQuery** – Frontend interactivity

## 🚀 Instalasi

```bash
# Clone repositori
git clone https://github.com/andrecode24/UTS-WEB-2025-ANDRE

# Masuk ke folder proyek
cd UTS-WEB-2025-ANDRE

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instal dependensi
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Seed database (optional - untuk testing)
python manage.py seed_data

# Jalankan development server
python manage.py runserver
```

Website akan berjalan di: **http://127.0.0.1:8000/**

## 🔑 Default Login Credentials

Setelah menjalankan `seed_data`:

**Admin**
- Email: `admin@prasetiyamulya.ac.id`
- Password: `admin123`

**Student (Sample)**
- Email: `budi.santoso@student.prasetiyamulya.ac.id`
- Password: `student123`

**Supervisor (Sample)**
- Email: `andi.wijaya@tokopedia.com`
- Password: `supervisor123`

## 📁 Struktur Aplikasi

```
UTS-WEB-2025-ANDRE/
├── accounts/          # User management & authentication
├── core/             # Core functionality & homepage
├── evaluations/      # Evaluation system (UTS/UAS)
├── internships/      # Job postings & placements
├── notifications/    # Notification system
├── reports/          # Monthly reports
├── templates/        # HTML templates
├── static/          # CSS, JS, images
└── media/           # User uploaded files
```

## 💡 Catatan

* Platform ini menggunakan email-based authentication dengan role-based access control
* File upload terbatas maksimal 5MB dengan validasi tipe file
* Responsive design untuk mobile, tablet, dan desktop
* Database default menggunakan SQLite

## 📄 Lisensi

[MIT](LICENSE) – bebas digunakan, silakan modifikasi sesuai kebutuhan.
