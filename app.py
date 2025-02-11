import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, request
import os
from dotenv import load_dotenv


load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Укажи свой URL
bot = telebot.TeleBot(TG_BOT_TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Принимает обновления от Telegram"""
    json_data = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(json_data)])
    return "OK", 200

@bot.message_handler(commands=['start'])
def start_handler(message):
    print("Получена команда /start")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    game_button = KeyboardButton(text="Играть!", web_app=WebAppInfo(url="https://devourer-f.github.io/Game/"))
    keyboard.add(game_button)

    bot.send_message(message.chat.id, "Нажмите 'Играть!', чтобы запустить игру.", reply_markup=keyboard)

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)  # Устанавливаем Webhook
    app.run(host='0.0.0.0', port=5000, debug=True)
