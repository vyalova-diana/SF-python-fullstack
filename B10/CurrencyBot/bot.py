import telebot
from config import *
from extensions import APIException, CurrencyConvert

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def greet(message: telebot.types.Message):
    text = "Для начала работы введите команду в следующем виде:\n " \
           "<имя валюты > <имя " \
           "валюты для перевода> <количество переводимой валюты>\n" \
           "Для вывода списка доступных валют: /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for _ in currencies.keys():
        text = '\n'.join((text, _,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        try:
            curr_from, curr_to, amount = message.text.split(" ")
        except ValueError:
            raise APIException("Слишком много параметров!")
        total = CurrencyConvert.get_price(curr_from, curr_to, amount)
    except APIException as ae:
        bot.send_message(message.chat.id, f"Ошибка пользователя:\n{ae}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось обработать команду:\n{e}")
    else:
        text = f"Цена {amount} {curr_from} в {curr_to} : {total}"
        bot.send_message(message.chat.id, text)


bot.polling()
