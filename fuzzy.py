import pandas as pd

# ==========================
# 1. Baca data dari file Excel
# ==========================
data = pd.read_excel("restoran.xlsx")

# ==========================
# 2. Fungsi Fuzzifikasi Pelayanan (Buruk, Sedang, Bagus)
# ==========================
def fuzzifikasi_pelayanan(nilai):
    # Bentuk fungsi segitiga untuk setiap kategori
    if nilai <= 50:
        buruk = (50 - nilai) / 50
    else:
        buruk = 0

    if 50 < nilai < 75:
        sedang = (nilai - 50) / 25
    elif 75 <= nilai <= 100:
        sedang = (100 - nilai) / 25
    else:
        sedang = 0

    if nilai >= 75:
        bagus = (nilai - 75) / 25
    else:
        bagus = 0

    return buruk, sedang, bagus

# ==========================
# 3. Fungsi Fuzzifikasi Harga (Murah, Sedang, Mahal)
# ==========================
def fuzzifikasi_harga(nilai):
    if nilai <= 25000:
        murah = 1
    elif nilai < 35000:
        murah = (35000 - nilai) / 10000
    else:
        murah = 0

    if 35000 < nilai < 45000:
        sedang = (nilai - 35000) / 10000
    elif 45000 <= nilai < 55000:
        sedang = (55000 - nilai) / 10000
    else:
        sedang = 0

    if nilai >= 55000:
        mahal = 1
    elif nilai > 45000:
        mahal = (nilai - 45000) / 10000
    else:
        mahal = 0

    return murah, sedang, mahal

# ==========================
# 4. Inferensi dan Defuzzifikasi (metode Weighted Average)
# ==========================
def hitung_kelayakan(pelayanan, harga):
    # Fuzzifikasi input
    buruk, sedang_p, bagus = fuzzifikasi_pelayanan(pelayanan)
    murah, sedang_h, mahal = fuzzifikasi_harga(harga)

    # Daftar aturan fuzzy yang aktif
    aturan = []

    # Aturan 1: Jika pelayanan sedang DAN harga murah → Layak (skor 75)
    if sedang_p > 0 and murah > 0:
        alpha = min(sedang_p, murah)
        aturan.append((alpha, 75))

    # Aturan 2: Jika pelayanan bagus DAN harga murah → Sangat Layak (skor 100)
    if bagus > 0 and murah > 0:
        alpha = min(bagus, murah)
        aturan.append((alpha, 100))

    # Defuzzifikasi menggunakan metode rata-rata berbobot
    if aturan:
        total_numerator = sum(a * z for a, z in aturan)
        total_denominator = sum(a for a, _ in aturan)
        skor_kelayakan = total_numerator / total_denominator
    else:
        skor_kelayakan = 0

    return skor_kelayakan

# ==========================
# 5. Hitung skor kelayakan untuk semua data
# ==========================
data["SKOR_KELAYAKAN"] = data.apply(
    lambda baris: hitung_kelayakan(baris["PELAYANAN"], baris["HARGA"]),
    axis=1
)

# ==========================
# 6. Ambil 5 restoran terbaik
# ==========================
top5 = data.sort_values("SKOR_KELAYAKAN", ascending=False).head(5)

# ==========================
# 7. Tampilkan hasil di terminal
# ==========================
print("=== 5 Restoran Terbaik Berdasarkan Sistem Fuzzy ===")
print(top5[["ID_PELANGGAN", "PELAYANAN", "HARGA", "SKOR_KELAYAKAN"]])

# ==========================
# 8.
