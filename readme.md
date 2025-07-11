# Sistem AHP untuk Penilaian Kenaikan Status Guru

Aplikasi berbasis Streamlit yang mengimplementasikan metode **Analytic Hierarchy Process (AHP)** untuk membantu penilaian kenaikan status guru di sekolah. Sistem ini memudahkan pengelolaan data guru, kriteria dan subkriteria penilaian, perhitungan bobot AHP, penilaian guru, serta menghasilkan ranking berdasarkan metode AHP.

---

## Fitur Utama

- **Manajemen Guru**: CRUD data guru dan jabatan.
- **Manajemen Kriteria & Subkriteria**: Input, edit, dan hapus kriteria penilaian serta subkriteria.
- **Perbandingan Berpasangan**: Input matriks perbandingan antar kriteria dan antar subkriteria.
- **Penilaian Guru**: Input manual atau import nilai subkriteria per guru.
- **Perhitungan AHP**: Menghitung bobot kriteria dan subkriteria, serta indeks konsistensi (CI, CR).
- **Perangkingan Guru**: Perhitungan skor total dan ranking guru berdasarkan bobot dan nilai.
- **Export PDF**: Export laporan ranking guru ke PDF.
- **Manajemen User & Role**: Sistem login dengan role admin dan user, pembatasan akses menu.
- **Dashboard Statistik**: Statistik jumlah guru, kriteria, subkriteria, dan pengguna.

---

## Teknologi

- Python 3.x
- Streamlit
- MySQL
- Pandas, NumPy
- Matplotlib
- ReportLab (PDF export)
- streamlit-option-menu (sidebar menu)

---

## Instalasi

1. Clone repository

```bash
git clone https://github.com/medynp/ahp_new.git
cd repository
```

2. Install Dependencies

```bash
pip install -r requirements.txt
```

3. Konfigurasi Database

```bash
Buat database baru

Jalankan skrip SQL untuk membuat tabel (guru, kriteria, subkriteria, nilai_subkriteria, perbandingan_kriteria, perbandingan_subkriteria, user)

Sesuaikan konfigurasi koneksi di database.py
```

4. jalankan Aplikasi

```bash
streamlit run app.py
```

## Contact
Meidi - meidiynp29@gmail.com

Project Link: [https://github.com/medynp/ahp_new.git]