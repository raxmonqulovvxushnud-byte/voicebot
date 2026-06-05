import os
import subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ConversationHandler, filters, ContextTypes

TOKEN = "8286492634:AAHF5NBCiz6TxfV1uLY52jWXyPwQeFtfJfY"

WAITING_TEXT = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Video yuboring — men uni golos + quote matn qilib beraman!"
    )

async def video_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏳ Video yuklanmoqda...")
    
    file = await update.message.video.get_file()
    await file.download_to_drive("input_video.mp4")
    
    context.user_data["has_video"] = True
    await msg.edit_text("✏️ Matnni kiriting:")
    return WAITING_TEXT

async def text_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await update.message.reply_text("⏳ Tayyorlanmoqda...")

    ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg")
    subprocess.run([
        ffmpeg_path, "-y", "-i", "input_video.mp4",
        "-vn", "-acodec", "libmp3lame", "output_audio.mp3"
    ])

    escaped = text.replace(".", "\\.").replace("!", "\\!").replace(
        "-", "\\-").replace("(", "\\(").replace(")", "\\)").replace(
        ">", "\\>").replace("#", "\\#").replace("+", "\\+").replace(
        "=", "\\=").replace("|", "\\|").replace("{", "\\{").replace(
        "}", "\\}").replace("~", "\\~").replace("`", "\\`").replace(
        "_", "\\_").replace("*", "\\*").replace("[", "\\[").replace(
        "]", "\\]")

    await update.message.reply_voice(
        voice=open("output_audio.mp3", "rb"),
        caption=f">{escaped}",
        parse_mode="MarkdownV2"
    )

    if os.path.exists("input_video.mp4"):
        os.remove("input_video.mp4")
    if os.path.exists("output_audio.mp3"):
        os.remove("output_audio.mp3")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.VIDEO, video_received)],
        states={
            WAITING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, text_received)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("✅ VoiceBot ishlamoqda...")
    app.run_polling()

if __name__ == "__main__":
    main()