IN236 Sistem Inventory
Sistem Inventory adalah aplikasi berbasis web untuk mengelola barang dan tipe barang, mencakup fitur CRUD, pencarian, pagination, dan validasi input.

Fitur
Manajemen Barang:
Tambah, Ubah, Hapus Barang.
Pencarian barang berdasarkan nama atau ID.
Pagination untuk navigasi data barang.
Manajemen Tipe Barang:
Tambah, Ubah, Hapus Tipe Barang.
Pencarian tipe barang berdasarkan nama.
Pagination untuk navigasi data tipe barang.
Validasi Input:
Validasi data untuk memastikan konsistensi dan keakuratan.
Export Data:
Ekspor data barang dan tipe barang ke format CSV.
Responsivitas:
Antarmuka yang dapat diakses di berbagai perangkat.
Teknologi yang Digunakan
Backend: Flask
Frontend: HTML, CSS (Bootstrap), JavaScript
Database: SQLite
Versi Python: 3.x
Instalasi
Clone repository:
bash
Copy code
git clone https://github.com/Kuroyukihime00/IN236_SistemInventory.git
Masuk ke direktori proyek:
bash
Copy code
cd IN236_SistemInventory
Buat virtual environment:
bash
Copy code
python -m venv venv
Aktifkan virtual environment:
Windows:
bash
Copy code
venv\Scripts\activate
Linux/Mac:
bash
Copy code
source venv/bin/activate
Instal dependensi:
bash
Copy code
pip install -r requirements.txt
Jalankan aplikasi:
bash
Copy code
python app.py
Akses aplikasi di browser:
arduino
Copy code
http://127.0.0.1:5000/
Struktur Proyek
app.py: File utama untuk backend aplikasi.
templates/: Folder untuk file HTML (frontend).
static/: Folder untuk file CSS, JavaScript, dan asset lainnya.
instance/: Database SQLite.
requirements.txt: Daftar dependensi Python.
Penggunaan
Dashboard Home:
Tampilan awal aplikasi.
Menu Barang:
Tambah, ubah, hapus, dan kelola barang.
Pencarian dan pagination untuk navigasi data.
Menu Tipe Barang:
Tambah, ubah, hapus, dan kelola tipe barang.
Pencarian dan pagination untuk navigasi data.
