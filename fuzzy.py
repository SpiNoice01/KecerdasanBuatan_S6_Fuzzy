import pandas as pd

# Baca data
df = pd.read_excel("restoran.xlsx")

# Fuzzifikasi Pelayanan
def fuzzifikasi_pelayanan(p):
    buruk = max(0, min(1, (50 - p) / 50)) if p <= 50 else 0
    sedang = (p - 50) / 25 if 50 < p < 75 else (100 - p) / 25 if 75 <= p <= 100 else 0
    bagus = max(0, min(1, (p - 75) / 25)) if p >= 75 else 0
    return buruk, sedang, bagus

# Fuzzifikasi Harga
def fuzzifikasi_harga(h):
    if h <= 25000:
        murah = 1
    elif h < 35000:
        murah = (35000 - h) / 10000
    else:
        murah = 0

    if 35000 < h < 45000:
        sedang = (h - 35000) / 10000
    elif 45000 <= h < 55000:
        sedang = (55000 - h) / 10000
    else:
        sedang = 0

    if h >= 55000:
        mahal = 1
    elif h > 45000:
        mahal = (h - 45000) / 10000
    else:
        mahal = 0

    return murah, sedang, mahal

# Inferensi dan Defuzzifikasi
def inferensi_defuzzifikasi(pelayanan, harga):
    buruk, sedang_p, bagus = fuzzifikasi_pelayanan(pelayanan)
    murah, sedang_h, mahal = fuzzifikasi_harga(harga)

    rules = []
    if sedang_p > 0 and murah > 0:
        rules.append((min(sedang_p, murah), 75))  # Layak
    if bagus > 0 and murah > 0:
        rules.append((min(bagus, murah), 100))    # Sangat Layak

    numerator = sum(a * z for a, z in rules)
    denominator = sum(a for a, _ in rules)
    return numerator / denominator if denominator else 0

# Proses semua data
df["SKOR_KELAYAKAN"] = df.apply(lambda row: inferensi_defuzzifikasi(row["PELAYANAN"], row["HARGA"]), axis=1)

# Ambil 5 terbaik
top5 = df.sort_values("SKOR_KELAYAKAN", ascending=False).head(5)

# Cetak ke terminal
print("Top 5 Restoran Terbaik Berdasarkan Sistem Fuzzy:")
print(top5[["ID_PELANGGAN", "PELAYANAN", "HARGA", "SKOR_KELAYAKAN"]])

# Simpan ke file
top5.to_excel("peringkat.xlsx", index=False)
