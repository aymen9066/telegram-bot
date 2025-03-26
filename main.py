from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, ContextTypes
from module1.join import Personne, Client, Voiture
from module1.storage import *
import requests, subprocess, time

# Telegram Bot Token
BOT_TOKEN : str|None = os.getenv("bot_token")
info_voiture_url : str = ""
if BOT_TOKEN is None:
    raise ValueError("can't find env variable bot_token!")

async def start(update : Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Command start was called.")
    if update.message is None or update.message.from_user is None:
        raise ValueError("No message found in the update!")
    print(f"{update.message.from_user}")
    user : Personne = Client(chat_id = update.message.chat_id
                             ,first_name = update.message.from_user.first_name
                             ,last_name = update.message.from_user.last_name
                             ,username = update.message.from_user.username
                             ,is_bot = update.message.from_user.is_bot
                             ,language_code = update.message.from_user.language_code)
    keyboard = [[InlineKeyboardButton("Entrez les information de votre vehicule", web_app= {"url": f"{site_url}/info-voiture?chat_id={user.chat_id}&user_id={user.id}"} )]]
    button_info_voiture = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bonjour je suis un bot de diagnostic des pannes automobiles!", reply_markup = button_info_voiture)

if __name__ == "__main__":
    #Gestion ngrok
    try:
        ngrok_status = requests.get("http://localhost:4040/api/tunnels")
        site_url = "https://375c-41-141-112-128.ngrok-free.app"
    except (Exception):
        print("starting ngrok...")
        ngrok_process = subprocess.Popen(["ngrok", "http", "5000"])
        time.sleep(1)
        site_url = requests.get("http://localhost:4040/api/tunnels").json()["tunnels"][0]["public_url"]
    #Gestion serveur
    log_file = open("flask_server.log", "w")
    serveur = subprocess.Popen(["python", "serveur-flask.py"], stdout = log_file, stderr = log_file)
    #Gestion bot
    app = Application.builder().token(BOT_TOKEN).build()
    print("Telegram bot has started...")
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

