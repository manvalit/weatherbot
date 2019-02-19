import telebot
import pyowm

bot = telebot.TeleBot('757986273:AAH2uu4cCJNzbaCzuZxvEVRy6ZDIALRcRD4')
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




while True:
    try:
        bot.polling(none_stop=True)
    except:
        pass