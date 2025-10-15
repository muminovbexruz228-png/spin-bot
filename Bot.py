import telebot
import random
from telebot import types

bot = telebot.TeleBot("BU_YERGA_TOKEN_QO'Y")

names = []
repeat_allowed = False

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎰 Salom! 'Spin Tanlov' botiga xush kelibsiz!\n\nIsmlarni vergul bilan ajratib kiriting:")

@bot.message_handler(func=lambda message: ',' in message.text)
def get_names(message):
    global names
    names = [i.strip() for i in message.text.split(',') if i.strip()]
    if len(names) < 2:
        bot.send_message(message.chat.id, "❗ Kamida 2 ta ism kiriting.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("✅ Ha", "❌ Yo‘q")
    bot.send_message(message.chat.id, "1ta ism 2-3 marta tushsinmi?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["✅ Ha", "❌ Yo‘q"])
def repeat_setting(message):
    global repeat_allowed
    repeat_allowed = message.text == "✅ Ha"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎯 Spin")
    bot.send_message(message.chat.id, "Ajoyib! Endi '🎯 Spin' bos!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🎯 Spin")
def spin(message):
    global names, repeat_allowed
    if not names:
        bot.send_message(message.chat.id, "❗ Avval ismlar kiriting.")
        return
    chosen = random.choice(names)
    bot.send_message(message.chat.id, f"🎉 Tanlov natijasi: *{chosen}*", parse_mode="Markdown")
    if not repeat_allowed:
        names.remove(chosen)
        if not names:
            bot.send_message(message.chat.id, "✅ Hammasi ishlatildi! /start bosing.")

bot.polling()
