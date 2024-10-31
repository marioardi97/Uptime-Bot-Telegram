import psutil
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio

# Masukkan token bot Telegram
BOT_TOKEN = 'TOKEN KALIAN'
chat_ids = set()  # Menyimpan beberapa chat ID
CPU_THRESHOLD = 80  # Ambang batas penggunaan CPU dalam persen
MEMORY_THRESHOLD = 80  # Ambang batas penggunaan memori dalam persen
DISK_THRESHOLD = 80  # Ambang batas penggunaan disk dalam persen

def get_resource_usage():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent  # Menambahkan pengecekan penggunaan disk
    return cpu, memory, disk

async def send_alert(context: CallbackContext, cpu_usage=None, memory_usage=None, disk_usage=None):
    message = "⚠️ Alert!"
    if cpu_usage is not None:
        message += f"\nCPU Usage: {cpu_usage}%"
    if memory_usage is not None:
        message += f"\nMemory Usage: {memory_usage}%"
    if disk_usage is not None:
        message += f"\nDisk Usage: {disk_usage}%"

    for chat_id in chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

async def check_resource_usage(context: CallbackContext):
    while True:
        cpu_usage, memory_usage, disk_usage = get_resource_usage()
        print(f"Current CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%, Disk Usage: {disk_usage}%")  # Debug log

        # Memeriksa ambang batas dan mengirim notifikasi jika perlu
        if cpu_usage > CPU_THRESHOLD:
            await send_alert(context, cpu_usage=cpu_usage)
        if memory_usage > MEMORY_THRESHOLD:
            await send_alert(context, memory_usage=memory_usage)
        if disk_usage > DISK_THRESHOLD:
            await send_alert(context, disk_usage=disk_usage)

        await asyncio.sleep(60)  # Cek setiap 60 detik

async def start(update: Update, context: CallbackContext):
    chat_ids.add(update.message.chat.id)
    await update.message.reply_text("Bot monitoring aktif! Anda akan menerima notifikasi.")

    # Kirim informasi penggunaan resource saat ini
    cpu, memory, disk = get_resource_usage()
    await context.bot.send_message(chat_id=update.message.chat.id, 
                                    text=f"🖥️ CPU Usage: {cpu}%\n💾 Memory Usage: {memory}%\n📀 Disk Usage: {disk}%")

async def monitor(update: Update, context: CallbackContext):
    cpu, memory, disk = get_resource_usage()
    await update.message.reply_text(f"✅ Server is UP!\n🖥️ CPU Usage: {cpu}%\n💾 Memory Usage: {memory}%\n📀 Disk Usage: {disk}%")

# Setup bot dan perintah
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("monitor", monitor))

# Jalankan cek penggunaan resource dalam thread terpisah
application.job_queue.run_repeating(check_resource_usage, interval=60, first=0)

# Menjalankan bot di event loop utama
application.run_polling()
