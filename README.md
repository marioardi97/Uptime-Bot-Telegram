![uptime](https://github.com/user-attachments/assets/d6b5dbd8-c7fa-44d2-8ece-27abe9a04eb2)
# Telegram Resource Monitoring Bot

Bot ini dirancang untuk memantau penggunaan sumber daya server Kalian, termasuk CPU dan memori, serta memberikan notifikasi melalui Telegram.

## Fitur

- Memantau penggunaan CPU dan memori.
- Mengirim notifikasi ke pengguna ketika bot diaktifkan.
- Memberikan informasi penggunaan sumber daya saat diminta.
- Memberikan Info ketika penggunaan berlebih dari set treshold

## Prerequisites

Sebelum menjalankan bot ini, pastikan Kalian telah menginstal Python 3.7 atau yang lebih baru di sistem Kalian. Kalian juga memerlukan beberapa paket yang diperlukan.

## Instalasi

1. **Clone repositori ini**:

   ```bash
   git clone https://github.com/marioardi97/Uptime-Bot-Telegram.git
   cd Uptime-Bot-Telegram

2. ** Instal Dependensi **
   ```Phyton
   pip install python-telegram-bot psutil

3. ** Token Chat Bot **
   Masukan Token Chat Bot Telegram Kalian ke dalam file pythonnya.

4. ** Penggunaan **
   /Start untuk memulai Bot
   /Monitor untuk melihat resource usage saat ini ( buat saja command ini pada bot, untuk memudahkan)
