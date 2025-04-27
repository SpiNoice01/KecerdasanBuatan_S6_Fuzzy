Deskripsi Umum
# Sistem Fuzzy Logic untuk Pemilihan Restoran Terbaik

Membangun sistem berbasis **Fuzzy Logic** untuk memilih **5 restoran terbaik** berdasarkan data dari file `restoran.xlsx`. Data yang tersedia memiliki tiga atribut:

- **ID Pelanggan**: ID yang diassign ke restoran.
- **Pelayanan**: Skor kualitas pelayanan (1 hingga 100).
- **Harga**: Harga rata-rata per orang di restoran (dalam IDR).

Sistem ini akan memilih 5 restoran terbaik berdasarkan **kualitas pelayanan** dan **harga** melalui proses **fuzzification**, **inferensi**, dan **defuzzification**.

---

## Kriteria yang Dihitung

### 1. Pelayanan
Menggunakan sistem fuzzy untuk mengklasifikasikan restoran berdasarkan skor pelayanan:
- **Sangat Buruk**: 0–20
- **Buruk**: 21–40
- **Cukup**: 41–60
- **Baik**: 61–80
- **Sangat Baik**: 81–100

### 2. Harga
Menilai harga berdasarkan kategori:
- **Murah**: 0–30,000
- **Sedang**: 30,001–50,000
- **Mahal**: 50,001–70,000
- **Sangat Mahal**: 70,001 ke atas

---

## Tujuan 👑👑👑👑
Output sistem adalah **5 restoran terbaik** berdasarkan skor pelayanan dan harga, dengan skor akhir hasil dari **defuzzification**. Setiap restoran dinilai berdasarkan dua atribut (**Pelayanan** dan **Harga**) menggunakan aturan fuzzy yang telah ditentukan.

---

## Langkah-langkah yang Harus Dilakukan

1. **Membaca Data** dari file `restoran.xlsx`.
2. **Fuzzification**: Mengubah skor pelayanan dan harga menjadi nilai fuzzy sesuai kategori yang telah ditentukan.
3. **Inferensi**: Menggunakan aturan fuzzy untuk menentukan kelayakan restoran berdasarkan kategori pelayanan dan harga.
4. **Defuzzification**: Menghitung nilai crisp (nilai final) berdasarkan aturan yang dibuat, kemudian menentukan urutan restoran berdasarkan skor kelayakan.
5. **Output**: Menampilkan 5 restoran terbaik dengan skor tertinggi berdasarkan perhitungan defuzzification.
6. **Menyimpan Hasil**: Menyimpan hasil peringkat restoran ke dalam file `peringkat.xlsx`.

---

## Input Data (`restoran.xlsx`)

| ID Pelanggan | Pelayanan | Harga  |
|--------------|-----------|--------|
| 1            | 29        | 42,675 |
| 2            | 30        | 45,791 |
| 3            | 71        | 34,107 |
| ...          | ...       | ...    |

---

## Batasan
- **Tidak boleh** menggunakan library yang menyediakan fungsi fuzzy logic siap pakai (contoh: Scikit-learn).
- **Boleh** menggunakan library lain hanya untuk keperluan membaca dan menyimpan file Excel (contoh: `pandas` atau `openpyxl`).
- Proses **Fuzzification**, **Inferensi**, dan **Defuzzification** harus dilakukan **manual**.

---

## Tools yang Diizinkan
- `pandas` untuk membaca dan menyimpan file Excel.
- Library standar Python (seperti `math`, `csv`, `openpyxl`).

---

## Output Program
Menampilkan daftar **5 restoran terbaik**, beserta:
- **ID Pelanggan**
- **Pelayanan** (kategori)
- **Harga** (kategori)
- **Skor kelayakan** (hasil defuzzification)

Menyimpan output ke file `peringkat.xlsx`.

---

## Pekerjaan Lain yang Perlu Dilakukan

### 1. Pembuatan Slide Presentasi
Isi utama dalam slide presentasi:
- Uraian masalah/persoalan.
- Hal-hal yang kelompok Anda kerjakan.
- Hasil/output serta analisis Anda terhadapnya.

**Format**: `.ppt`, `.pptx`, atau `.pdf`.  
**Durasi Presentasi**: Maksimal 5 menit, dengan tanya-jawab hingga 15 menit.

### 2. Penyusunan Laporan Tugas
Isi laporan tugas:
- Deskripsi masalah/persoalan.
- Seluruh poin yang harus didesain dan dianalisis.
- Output yang dihasilkan oleh program Anda.

**Catatan**:
- Gaya tulisan laporan bebas; dikumpulkan dalam format `.PDF`.
- Ketidaksesuaian antara laporan dengan kode program akan memengaruhi nilai.
- Cantumkan **screenshot hasil running program** berdasarkan sistem fuzzy yang dibuat.
- Tuliskan **peran anggota kelompok**, termasuk jika ada yang tidak berperan sama sekali.

