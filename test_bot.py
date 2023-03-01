# Изначально писал код обучаюсь на ютубе, так как на платформе был сбой.
# Бот отлично работал когда был на одной странице. Не было никаких повторных ненужных сообщений.
# Но после того как курс открылся и я увидел усложнения в виде статистического метода, пришлось все рушить.
# В итоге сейчас он работает не идеально и я не могу это исправить, не понимаю как.


from extensions import TOKEN, Exchange

import telebot
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    t = 'Чтобы начать введите команду в следующем формате через пробел: \n<имя валюты> \n<в какую валюту конвертировать> ' \
'\n<количество> \n<Введите "/values" чтобы увидеть список доступных валют> \n<дробные части разделять точкой'
    bot.reply_to(message, t)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    t2 = 'Доступные валюты: \nzcash \nbitcoin \nethereum'
    bot.reply_to(message, t2)

@bot.message_handler(content_types=['text', ])
def cours(message: telebot.types.Message):
    v = message.text.split(' ')
    if len(v) != 3:
        bot.send_message(message.chat.id, "Неверный формат ввода")
        return values
    base, quote, amount = v
    x = Exchange.exc(base, quote, amount, message)
    text = f'Цена {amount} {base} в {quote}  = {x}'
    bot.send_message(message.chat.id, text)
bot.polling(none_stop=True)