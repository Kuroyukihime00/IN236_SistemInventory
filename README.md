# IN236 Sistem Inventory

Sistem Inventory adalah aplikasi berbasis web untuk mengelola barang dan tipe barang, mencakup fitur CRUD, pencarian, pagination, dan validasi input.

## Fitur
- **Manajemen Barang:**
  - Tambah, Ubah, Hapus Barang.
  - Pencarian barang berdasarkan nama atau ID.
  - Pagination untuk navigasi data barang.
- **Manajemen Tipe Barang:**
  - Tambah, Ubah, Hapus Tipe Barang.
  - Pencarian tipe barang berdasarkan nama.
  - Pagination untuk navigasi data tipe barang.
- **Validasi Input:**
  - Validasi data untuk memastikan konsistensi dan keakuratan.
- **Export Data:**
  - Ekspor data barang dan tipe barang ke format CSV.
- **Responsivitas:**
  - Antarmuka yang dapat diakses di berbagai perangkat.

## Teknologi yang Digunakan
- **Backend:** Flask
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Database:** SQLite
- **Versi Python:** 3.x

## Instalasi
1. Clone repository:
   ```bash
   git clone https://github.com/Kuroyukihime00/IN236_SistemInventory.git
   ```
2. Masuk ke direktori proyek:
   ```bash
   cd IN236_SistemInventory
   ```
3. Buat virtual environment:
   ```bash
   python -m venv venv
   ```
4. Aktifkan virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```
5. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
6. Jalankan aplikasi:
   ```bash
   python app.py
   ```
7. Akses aplikasi di browser:
   ```
   http://127.0.0.1:5000/
   ```

## Struktur Proyek
- **app.py:** File utama untuk backend aplikasi.
- **templates/**: Folder untuk file HTML (frontend).
- **static/**: Folder untuk file CSS, JavaScript, dan asset lainnya.
- **instance/**: Database SQLite.
- **requirements.txt:** Daftar dependensi Python.

## Penggunaan
1. **Dashboard Home:**
   - Tampilan awal aplikasi.
2. **Menu Barang:**
   - Tambah, ubah, hapus, dan kelola barang.
   - Pencarian dan pagination untuk navigasi data.
3. **Menu Tipe Barang:**
   - Tambah, ubah, hapus, dan kelola tipe barang.
   - Pencarian dan pagination untuk navigasi data.

## Kontribusi
1. Fork repository ini.
2. Buat branch fitur baru:
   ```bash
   git checkout -b fitur-anda
   ```
3. Commit perubahan Anda:
   ```bash
   git commit -m "Menambahkan fitur baru"
   ```
4. Push branch ke repository Anda:
   ```bash
   git push origin fitur-anda
   ```
5. Buat Pull Request ke branch `main`.

## Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).
