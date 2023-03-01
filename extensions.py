class NoFloat(Exception):
    pass
import telebot
#from test_bot import values
TOKEN = '6256636335:AAF56cH_nI95wgKssc9Bq7JIVl3V0zrzqXI'
bot = telebot.TeleBot(TOKEN)
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

class Exchange:
    @staticmethod
    def exc(base: str, quote: str, amount: str, message: telebot.types.Message):
        try:
            amount = float(amount)
            if base != "zcash" and base != "ethereum" and base != "bitcoin":
                bot.send_message(message.chat.id, "Введите валюты из списка")
                return values
            if quote != "zcash" and quote != "bitcoin" and quote != "ethereum":
                bot.send_message(message.chat.id, "Введите валюты из списка")
                return values
            if quote == base:
                bot.send_message(message.chat.id, "Введите разные валюты")
                return values
        except NoFloat as e:
            bot.reply_to(message, f'Ошибка ввода. \n{e}')
        except Exception as e:
            bot.reply_to(message, f'Проверьте правильность ввода данных. \n{e}')
        else:
            price1 = cg.get_price(ids=base, vs_currencies='usd')
            price2 = cg.get_price(ids=quote, vs_currencies='usd')
            x = (((price1[base]["usd"]) / (price2[quote]["usd"])) * float(amount))
            return x