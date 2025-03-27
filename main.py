import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, ContextTypes
from module1.join import *
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
    user : Personne = Client.create_from_telegram_user(update.message.chat_id, update.message.from_user)
    #keyboard = [[InlineKeyboardButton("Entrez les information de votre vehicule", web_app= {"url": f"{site_url}/info-voiture?chat_id={user.chat_id}&user_id={user.id}"} )]]
    keyboard = [[InlineKeyboardButton("Entrez les information de votre vehicule", web_app= WebAppInfo(f"{site_url}/info-voiture?chat_id={user.chat_id}&user_id={user.id}"))]]
    button_info_voiture = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bonjour je suis un bot de diagnostic des pannes automobiles!", reply_markup = button_info_voiture)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert(update.message is not None)
    assert(update.message.text is not None and update.message.from_user is not None)
    user: Personne = Client.create_from_telegram_user(update.message.chat_id, update.message.from_user)
    user.find_cars()
    print(user)
    print(f"the message number {update.message.message_id} was received : {update.message.text}")
    model = Model.create("deepseek", user.chat_id)
    if update.message.text.lower() == "test":
        await update.message.reply_text("testing...")
        return
    Storable.insert_message(user.chat_id, user.id, update.message.message_id, update.message.text)
    if len(user.cars) > 0:
        car : Voiture = user.cars[len(user.cars)-1]
        model.personal_context["car"] = (f"Ma voiture est une {car.brand},{car.model} "
                                         f"produit en {car.production_year} avec un killometrage de {car.km}")
    answer = model.prompt(update.message.text)
    Storable.insert_message(user.chat_id, 1, update.message.message_id+1, answer)
    await update.message.reply_text(answer)

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
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.run_polling()

