import pandas as pd

# Fungsi untuk membaca data dari file Excel
def baca_data_excel(file_path):
    return pd.read_excel(file_path)

# Fungsi Fuzzifikasi untuk atribut pelayanan
def fuzzifikasi_pelayanan(pelayanan):
    fuzzy = {
        'buruk': 0,
        'sedang': 0,
        'bagus': 0
    }
    if pelayanan <= 50:
        fuzzy['buruk'] = 1
    elif 50 < pelayanan <= 75:
        fuzzy['buruk'] = (75 - pelayanan) / 25
        fuzzy['sedang'] = (pelayanan - 50) / 25
    elif 75 < pelayanan <= 100:
        fuzzy['sedang'] = (100 - pelayanan) / 25
        fuzzy['bagus'] = (pelayanan - 75) / 25
    else:
        fuzzy['bagus'] = 1
    return fuzzy

# Fungsi Fuzzifikasi untuk atribut harga
def fuzzifikasi_harga(harga):
    fuzzy = {
        'murah': 0,
        'sedang': 0,
        'mahal': 0
    }
    if harga <= 35000:
        fuzzy['murah'] = 1
    elif 35000 < harga <= 50000:
        fuzzy['murah'] = (50000 - harga) / 15000
        fuzzy['sedang'] = (harga - 35000) / 15000
    elif 50000 < harga <= 55000:
        fuzzy['sedang'] = (55000 - harga) / 5000
        fuzzy['mahal'] = (harga - 50000) / 5000
    else:
        fuzzy['mahal'] = 1
    return fuzzy

# Fungsi Inferensi Fuzzy
def inferensi(fuzzy_pelayanan, fuzzy_harga):
    rules = {
        ('buruk', 'murah'): 'layak',
        ('sedang', 'murah'): 'layak',
        ('bagus', 'murah'): 'sangat_layak',
    }

    hasil = []
    for pelayanan_key, pelayanan_val in fuzzy_pelayanan.items():
        for harga_key, harga_val in fuzzy_harga.items():
            if (pelayanan_key, harga_key) in rules:
                keputusan = rules[(pelayanan_key, harga_key)]
                derajat = min(pelayanan_val, harga_val)
                if derajat > 0:
                    hasil.append((keputusan, derajat))

    return hasil

# Fungsi Defuzzifikasi
def defuzzifikasi(hasil_inferensi):
    nilai_keputusan = {
        'tidak_layak': 25,
        'kurang_layak': 50,
        'layak': 75,
        'sangat_layak': 100
    }

    if not hasil_inferensi:
        return 0

    total_numerator = 0
    total_denominator = 0

    for keputusan, derajat in hasil_inferensi:
        nilai = nilai_keputusan[keputusan]
        total_numerator += derajat * nilai
        total_denominator += derajat

    if total_denominator == 0:
        return 0
    return total_numerator / total_denominator

# Fungsi utama
def main():
    # Baca data dari file
    data = baca_data_excel('restoran.xlsx')

    hasil_akhir = []

    # Proses setiap baris
    for index, row in data.iterrows():
        pelayanan = row['PELAYANAN']
        harga = row['HARGA']

        fuzzy_pelayanan = fuzzifikasi_pelayanan(pelayanan)
        fuzzy_harga = fuzzifikasi_harga(harga)

        hasil_inferensi = inferensi(fuzzy_pelayanan, fuzzy_harga)
        nilai_defuzzifikasi = defuzzifikasi(hasil_inferensi)

        # Ambil keputusan fuzzy dominan berdasarkan total derajat
        if hasil_inferensi:
            derajat_total = {}
            for keputusan, derajat in hasil_inferensi:
                derajat_total[keputusan] = derajat_total.get(keputusan, 0) + derajat

            keputusan = max(derajat_total.items(), key=lambda x: x[1])[0]
            derajat = derajat_total[keputusan]
        else:
            keputusan, derajat = ('tidak_layak', 0)

        hasil_akhir.append({
            'ID_PELANGGAN': row['ID_PELANGGAN'],
            'Pelayanan': pelayanan,
            'Harga': harga,
            'Keputusan Fuzzy': keputusan,
            'Derajat Keanggotaan': derajat,
            'Nilai Defuzzifikasi': nilai_defuzzifikasi
        })

    # Ubah menjadi DataFrame
    df_hasil = pd.DataFrame(hasil_akhir)

    # Sortir berdasarkan Nilai Defuzzifikasi (besar ke kecil)
    df_sorted = df_hasil.sort_values(by='Nilai Defuzzifikasi', ascending=False)

    # Ambil Top 90 restoran terbaik
    df_top90 = df_sorted.head(90)

    # Simpan ke file Excel baru
    df_top90.to_excel('peringkat.xlsx', index=False)

    print("\nTop 90 restoran terbaik telah disimpan ke 'peringkat.xlsx' ")
    print(df_top90)

if __name__ == "__main__":
    main()