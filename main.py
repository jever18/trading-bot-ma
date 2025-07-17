from forex_python.converter import CurrencyRates
import pandas as pd
import matplotlib.pyplot as plt
import time
import requests

# GANTI dengan milikmu:
token = '8154774251:AAGyIrF_NqfgBoKAiLJCja87yub1j1Vllf4'
chat_id = '6345970865'  # contoh: '123456789'

# Fungsi kirim pesan ke Telegram
def kirim_telegram(pesan):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': pesan}
    requests.post(url, data=payload)

# Kirim notifikasi awal saat bot mulai jalan
kirim_telegram("🤖 Bot trading sudah aktif! Memantau sinyal MA5 vs MA10 setiap 30 detik.")

# Simpan data harga untuk perhitungan MA
harga_list = []

# Jalankan terus-menerus (real-time loop)
while True:
    try:
        # Ambil harga tukar USD ke EUR
        url = 'https://api.exchangerate.host/convert?from=USD&to=EUR'
        response = requests.get(url)
        data = response.json()
        harga = round(data['result'], 5)

        # Simpan harga
        harga_list.append(harga)

        # Tampilkan ke console (Pydroid)
        print(f'Harga terbaru: {harga}')

        # Jika data cukup untuk MA10
        if len(harga_list) >= 10:
            df = pd.DataFrame(harga_list, columns=['Harga'])
            df['MA5'] = df['Harga'].rolling(window=5).mean()
            df['MA10'] = df['Harga'].rolling(window=10).mean()

            # Ambil 2 titik terakhir untuk deteksi crossing
            prev_ma5 = df['MA5'].iloc[-2]
            prev_ma10 = df['MA10'].iloc[-2]
            now_ma5 = df['MA5'].iloc[-1]
            now_ma10 = df['MA10'].iloc[-1]

            # Deteksi sinyal
            if prev_ma5 < prev_ma10 and now_ma5 > now_ma10:
                kirim_telegram(f'📈 Sinyal BUY terdeteksi!\nHarga: {harga}\nMA5 naik potong MA10.')
            elif prev_ma5 > prev_ma10 and now_ma5 < now_ma10:
                kirim_telegram(f'📉 Sinyal SELL terdeteksi!\nHarga: {harga}\nMA5 turun potong MA10.')
            else:
                print("⏳ Tidak ada sinyal crossover MA.")

        # Tunggu 30 detik sebelum cek lagi
        time.sleep(30)

    except Exception as e:
        print(f'❌ Error: {e}')
        time.sleep(30)