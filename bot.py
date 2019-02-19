import telebot
import pyowm
import os
from flask import Flask, request
import logging
bot = telebot.TeleBot('')
def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"
def text(m):
    bot.send_message(m.chat.id, '_Напишите мне название города:_', parse_mode='Markdown')
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'Добро пожаловать в бот *☀Погода*! С помощью этого бота вы сможете узнать погоду в любом городе, поселке или же деревни!\n\n*P.S.* _Если вы хотите узнать погоду в местностях, которые находятся за пределами СНГ, то пишите название той или иной местности на английском языке._', parse_mode='Markdown')
    text(m)
@bot.message_handler(content_types=['text'])
def pogoda(m):
    bot.send_chat_action(m.chat.id, 'typing')
    try:
        owm = pyowm.OWM('8554a59e358f34662a01ac2e075daee6', language='ru')
        observation = owm.weather_at_place(str(m.text))
        w = observation.get_weather()
        tempira = w.get_temperature('celsius')['temp']
        tempir = toFixed(tempira, 1)
        stat = w.get_detailed_status()
        bot.send_message(m.chat.id, '_В городе/посёлке_ ' + '*' + str(m.text) + ' ' + str(
            tempir) + '* _градусов по Цельсию, ' + stat + '!_', parse_mode='Markdown')
    except:
        bot.send_message(m.chat.id, 'Вы ввели неверный город, попробуйте снова!')



if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://mvweatherbot.herokuapp.com/") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)