import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ConversationHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")

WAITING_TEXT = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Video yuboring — men uni golos + quote matn qilib beraman!"
    )

async def text_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    file_id = context.user_data.get("file_id")

    msg = await update.message.reply_text("⏳ Tayyorlanmoqda...")

    file = await context.bot.get_file(file_id)
    await file.download_to_drive("input_video.mp4")

    os.system("ffmpeg -y -i input_video.mp4 -vn -acodec libmp3lame output_audio.mp3")

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

    await msg.delete()
    return ConversationHandler.END

async def text_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    file_id = context.user_data.get("file_id")

    msg = await update.message.reply_text("⏳ Tayyorlanmoqda...")

    file = await context.bot.get_file(file_id)
    await file.download_to_drive("input_video.mp4")

    audio = AudioSegment.from_file("input_video.mp4")
    audio.export("output_audio.mp3", format="mp3")

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

    await msg.delete()
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