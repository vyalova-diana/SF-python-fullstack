import telebot
import json
import requests
from config import currencies


class APIException(Exception):
    pass


class CurrencyConvert:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException("Одинаковые валюты!")

        try:
            ticker_base = currencies[base]
        except KeyError:
            raise APIException(f"Некорректное название валюты! {base}")

        try:
            ticker_quote = currencies[quote]
        except KeyError:
            raise APIException(f"Некорректное название валюты! {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Некорректный формат количества валюты!")
        if amount <= 0:
            raise APIException("Некорректное количество валюты!")
        r = requests.get(f'https://free.currconv.com/api/v7/convert?q={ticker_base}_{ticker_quote}'
                         '&compact=ultra&apiKey=4d3d6a711c7513ee5fbd')
        rate = json.loads(r.content)[ticker_base + '_' + ticker_quote]
        return rate * amount
