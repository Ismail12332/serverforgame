import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, request
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Укажи свой URL

    # Создаем объект бота
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

    # Установка вебхука
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)  # Устанавливаем вебхук

    if __name__ == "__main__":
        app.run(debug=True)
    
    return app

