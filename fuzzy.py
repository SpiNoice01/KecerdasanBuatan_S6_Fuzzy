import pandas as pd

# --------------------
# Fungsi Membaca Data
# --------------------
def baca_data_excel(file_path):
    return pd.read_excel(file_path)

# --------------------
# Fungsi Fuzzifikasi Pelayanan Linear Segitiga
# --------------------
def fuzzifikasi_pelayanan(pelayanan):
    fuzzy = {}

    # Rendah (0-30)
    if pelayanan <= 30:
        fuzzy['rendah'] = 1
    elif 30 < pelayanan < 60:
        fuzzy['rendah'] = (60 - pelayanan) / (60 - 30)
    else:
        fuzzy['rendah'] = 0

    # Sedang (30-60-80)
    if 30 < pelayanan < 60:
        fuzzy['sedang'] = (pelayanan - 30) / (60 - 30)
    elif 60 <= pelayanan <= 80:
        fuzzy['sedang'] = (80 - pelayanan) / (80 - 60)
    else:
        fuzzy['sedang'] = 0

    # Tinggi (60-100)
    if pelayanan >= 60:
        if pelayanan <= 100:
            fuzzy['tinggi'] = (pelayanan - 60) / (100 - 60)
        else:
            fuzzy['tinggi'] = 1
    else:
        fuzzy['tinggi'] = 0

    return fuzzy

# --------------------
# Fungsi Fuzzifikasi Harga Linear Segitiga
# --------------------
def fuzzifikasi_harga(harga):
    fuzzy = {}

    # Murah (0-30k)
    if harga <= 30000:
        fuzzy['murah'] = 1
    elif 30000 < harga < 50000:
        fuzzy['murah'] = (50000 - harga) / (50000 - 30000)
    else:
        fuzzy['murah'] = 0

    # Sedang (30k-50k-70k)
    if 30000 < harga < 50000:
        fuzzy['sedang'] = (harga - 30000) / (50000 - 30000)
    elif 50000 <= harga <= 70000:
        fuzzy['sedang'] = (70000 - harga) / (70000 - 50000)
    else:
        fuzzy['sedang'] = 0

    # Mahal (50k-70k-100k)
    if 50000 < harga < 70000:
        fuzzy['mahal'] = (harga - 50000) / (70000 - 50000)
    elif harga >= 70000:
        fuzzy['mahal'] = 1
    else:
        fuzzy['mahal'] = 0

    return fuzzy

# --------------------
# Aturan Inferensi
# --------------------
def inferensi(fuzzy_pelayanan, fuzzy_harga):
    rules = {
        ('rendah', 'mahal'): 'tidak_layak',
        ('rendah', 'sedang'): 'kurang_layak',
        ('rendah', 'murah'): 'kurang_layak',
        ('sedang', 'mahal'): 'kurang_layak',
        ('sedang', 'sedang'): 'layak',
        ('sedang', 'murah'): 'layak',
        ('tinggi', 'mahal'): 'layak',
        ('tinggi', 'sedang'): 'sangat_layak',
        ('tinggi', 'murah'): 'sangat_layak',
    }

    hasil = []
    for pelayanan_key, pelayanan_val in fuzzy_pelayanan.items():
        for harga_key, harga_val in fuzzy_harga.items():
            if (pelayanan_key, harga_key) in rules:
                keputusan = rules[(pelayanan_key, harga_key)]
                derajat = min(pelayanan_val, harga_val)
                hasil.append((keputusan, derajat))

    if hasil:
        # Ambil keputusan dengan derajat keanggotaan paling tinggi
        hasil.sort(key=lambda x: x[1], reverse=True)
        return hasil[0]
    else:
        return ('tidak_layak', 0)

# --------------------
# Mapping Keputusan ke Nilai Crisp
# --------------------
crisp_value = {
    'tidak_layak': 25,
    'kurang_layak': 50,
    'layak': 75,
    'sangat_layak': 100
}

# --------------------
# Fungsi Defuzzifikasi
# --------------------
def defuzzifikasi(keputusan, derajat):
    nilai = crisp_value[keputusan]
    return derajat * nilai

# --------------------
# Main Program
# --------------------
def main():
    # Baca data
    data = baca_data_excel('restoran.xlsx')

    hasil_akhir = []

    # Proses setiap baris
    for index, row in data.iterrows():
        pelayanan = row['PELAYANAN']
        harga = row['HARGA']

        fuzzy_pelayanan = fuzzifikasi_pelayanan(pelayanan)
        fuzzy_harga = fuzzifikasi_harga(harga)

        keputusan, derajat = inferensi(fuzzy_pelayanan, fuzzy_harga)

        nilai_defuzzifikasi = defuzzifikasi(keputusan, derajat)

        hasil_akhir.append({
            'ID_PELANGGAN': row['ID_PELANGGAN'],
            'Pelayanan': pelayanan,
            'Harga': harga,
            'Keputusan Fuzzy': keputusan,
            'Derajat Keanggotaan': derajat,
            'Nilai Defuzzifikasi': nilai_defuzzifikasi
        })

    # Ubah ke DataFrame
    df_hasil = pd.DataFrame(hasil_akhir)

    # Sortir berdasarkan Nilai Defuzzifikasi (Terbaik ke Terburuk)
    df_sorted = df_hasil.sort_values(by='Nilai Defuzzifikasi', ascending=False)

    # Ambil Top 5
    df_top5 = df_sorted.head(5)

    # Simpan ke file baru
    df_top5.to_excel('hasil_top5.xlsx', index=False)

    print("\nTop 5 hasil terbaik telah disimpan ke 'hasil_top5.xlsx' 🎯")
    print(df_top5)

if __name__ == "__main__":
    main()
