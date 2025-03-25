from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, ContextTypes
import os

# Telegram Bot Token
BOT_TOKEN : str|None = os.getenv("bot_token")
if BOT_TOKEN is None:
    raise ValueError("can't find env variable bot_token!")

async def start(update : Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.from_user is None:
        raise ValueError("No message found in the update!")
    await update.message.reply_text("Bonjour je suis un bot de diagnostic des pannes automobiles!")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
    print("This is a telegram bot another")

