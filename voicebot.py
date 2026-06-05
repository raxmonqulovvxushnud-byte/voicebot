import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ConversationHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")
WAITING_TEXT = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Video yuboring — men uni golos + quote matn qilib beraman!"
    )

async def video_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["file_id"] = update.message.video.file_id
    await update.message.reply_text("✏️ Matnni kiriting:")
    return WAITING_TEXT

async def text_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    file_id = context.user_data.get("file_id")

    escaped = text.replace(".", "\\.").replace("!", "\\!").replace(
        "-", "\\-").replace("(", "\\(").replace(")", "\\)").replace(
        ">", "\\>").replace("#", "\\#").replace("+", "\\+").replace(
        "=", "\\=").replace("|", "\\|").replace("{", "\\{").replace(
        "}", "\\}").replace("~", "\\~").replace("`", "\\`").replace(
        "_", "\\_").replace("*", "\\*").replace("[", "\\[").replace(
        "]", "\\]")

    await update.message.reply_video(
        video=file_id,
        caption=f">{escaped}",
        parse_mode="MarkdownV2"
    )
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