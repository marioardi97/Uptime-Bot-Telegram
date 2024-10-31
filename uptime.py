import psutil
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Masukkan token bot Telegram
BOT_TOKEN = 'BOT TOKEN TELE KALIAN DISINI'
chat_ids = set()  # Menyimpan beberapa chat ID, Ini agar bisa digunakan untuk beberapa user

def get_resource_usage():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return (
        f"🖥️ CPU Usage: {cpu}%\n"
        f"💾 Memory Usage: {memory.percent}%\n"
        f"📀 Disk Usage: {disk.percent}%"
    )

async def start(update: Update, context: CallbackContext):
    chat_ids.add(update.message.chat_id)
    await update.message.reply_text("Bot monitoring aktif! Anda akan menerima notifikasi.")

    # Kirim informasi penggunaan resource saat ini
    usage_info = get_resource_usage()
    await context.bot.send_message(chat_id=update.message.chat_id, text=usage_info)

async def monitor(update: Update, context: CallbackContext):
    status_message = "✅ Server is UP!"
    usage_info = get_resource_usage()
    await update.message.reply_text(f"{status_message}\n{usage_info}")

# Setup bot dan perintah
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("monitor", monitor))

# Menjalankan bot di event loop utama
application.run_polling()
