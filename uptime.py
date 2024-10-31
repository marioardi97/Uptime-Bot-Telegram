import psutil
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio

# Masukkan token bot Telegram
BOT_TOKEN = 'TOKEN KALIAN'
chat_ids = set()  # Menyimpan beberapa chat ID
CPU_THRESHOLD = 80  # Ambang batas penggunaan CPU dalam persen
MEMORY_THRESHOLD = 80  # Ambang batas penggunaan memori dalam persen

def get_resource_usage():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    return cpu, memory.percent

async def send_alert(context: CallbackContext, cpu_usage, memory_usage):
    message = f"⚠️ Alert! CPU Usage: {cpu_usage}%\n⚠️ Alert! Memory Usage: {memory_usage}%"
    for chat_id in chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

async def check_resource_usage(context: CallbackContext):
    while True:
        cpu_usage, memory_usage = get_resource_usage()
        print(f"Current CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")  # Debug log
        if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD:
            print("Threshold exceeded! Sending alert...")  # Debug log
            await send_alert(context, cpu_usage, memory_usage)
        await asyncio.sleep(60)  # Cek setiap 60 detik

async def start(update: Update, context: CallbackContext):
    chat_ids.add(update.message.chat.id)
    await update.message.reply_text("Bot monitoring aktif! Anda akan menerima notifikasi.")

    # Kirim informasi penggunaan resource saat ini
    cpu, memory = get_resource_usage()
    await context.bot.send_message(chat_id=update.message.chat.id, text=f"🖥️ CPU Usage: {cpu}%\n💾 Memory Usage: {memory}%")

async def monitor(update: Update, context: CallbackContext):
    cpu, memory = get_resource_usage()
    await update.message.reply_text(f"✅ Server is UP!\n🖥️ CPU Usage: {cpu}%\n💾 Memory Usage: {memory}%")

# Setup bot dan perintah
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("monitor", monitor))

# Jalankan cek penggunaan resource dalam thread terpisah
application.job_queue.run_repeating(check_resource_usage, interval=60, first=0)

# Menjalankan bot di event loop utama
application.run_polling()
