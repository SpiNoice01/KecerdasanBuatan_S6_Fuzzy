import pandas as pd

# 1. Baca data dari file Excel
data = pd.read_excel("restoran.xlsx")

# 2. Fuzzifikasi: Mengubah nilai numerik menjadi derajat keanggotaan fuzzy untuk PELAYANAN
def fuzzifikasi_pelayanan(nilai):
    buruk = max(0, (50 - nilai) / 50) if nilai <= 50 else 0

    if 50 < nilai < 75:
        sedang = (nilai - 50) / 25
    elif 75 <= nilai <= 100:
        sedang = (100 - nilai) / 25
    else:
        sedang = 0

    bagus = max(0, (nilai - 75) / 25) if nilai >= 75 else 0

    return buruk, sedang, bagus

# 3. Fuzzifikasi: Mengubah nilai numerik menjadi derajat keanggotaan fuzzy untuk HARGA
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

# 4. Fungsi interpretasi skor numerik menjadi kategori kelayakan
def interpretasi_kelayakan(skor):
    if skor < 40:
        return "Tidak Layak"
    elif skor < 60:
        return "Kurang Layak"
    elif skor < 80:
        return "Layak"
    else:
        return "Sangat Layak"

# 5. Proses fuzzy: INFERENSI + DEFUZZIFIKASI
def hitung_kelayakan(pelayanan, harga):
    # ====== FUZZIFIKASI ======
    buruk, sedang_p, bagus = fuzzifikasi_pelayanan(pelayanan)
    murah, sedang_h, mahal = fuzzifikasi_harga(harga)

    # ====== INFERENSI ======
    # Gunakan aturan fuzzy untuk menentukan output kelayakan berdasarkan kombinasi pelayanan & harga
    aturan_logika = [
        (buruk, murah, 50),     # Buruk & Murah → Kurang Layak
        (buruk, sedang_h, 25),  # Buruk & Sedang → Tidak Layak
        (buruk, mahal, 25),     # Buruk & Mahal → Tidak Layak
        (sedang_p, murah, 75),  # Sedang & Murah → Layak
        (sedang_p, sedang_h, 50), # Sedang & Sedang → Kurang Layak
        (sedang_p, mahal, 25),  # Sedang & Mahal → Tidak Layak
        (bagus, murah, 100),    # Bagus & Murah → Sangat Layak
        (bagus, sedang_h, 75),  # Bagus & Sedang → Layak
        (bagus, mahal, 50),     # Bagus & Mahal → Kurang Layak
    ]

    aturan = []  # daftar aturan aktif: (nilai alpha, nilai output)
    for p, h, output in aturan_logika:
        alpha = min(p, h)  # ambil minimum dari dua nilai derajat keanggotaan (AND fuzzy)
        if alpha > 0:
            aturan.append((alpha, output))  # simpan jika aturan aktif

    # ====== DEFUZZIFIKASI ======
    # Gunakan metode Weighted Average (rata-rata berbobot)
    if aturan:
        total_num = sum(a * z for a, z in aturan)
        total_den = sum(a for a, _ in aturan)
        skor = total_num / total_den
    else:
        skor = 0  # Jika tidak ada aturan aktif

    return skor

# 6. Hitung kelayakan dan interpretasinya untuk semua data
data["SKOR_KELAYAKAN"] = data.apply(
    lambda row: hitung_kelayakan(row["PELAYANAN"], row["HARGA"]),
    axis=1
)
data["KETERANGAN"] = data["SKOR_KELAYAKAN"].apply(interpretasi_kelayakan)

# 7. Ambil 5 restoran terbaik
top5 = data.sort_values("SKOR_KELAYAKAN", ascending=False).head(5)

# 8. Tampilkan hasil ke terminal
print("=== 5 Restoran Terbaik Berdasarkan Sistem Fuzzy ===")
print(top5[["ID_PELANGGAN", "PELAYANAN", "HARGA", "SKOR_KELAYAKAN", "KETERANGAN"]])

# 9. Simpan ke Excel
top5.to_excel("peringkat.xlsx", index=False)
