import json
import requests
from config import key

# Создаем собственный класс исключения
class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        # Проверяем, что введенная базовая валюта есть в словаре
        try:
            base_key = key[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        # Проверяем, что конвертируемая валюта есть в словаре
        try:
            quote_key = key[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        # Выводим исключение, если пользователь пытается перевести в одну и ту же валюту
        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        # Проверяем, чтобы количество было числом и выводим исключение, если это не так
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        # Формируем запрос к API, подставляем динамически данные от пользователя
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}")
        # Преобразовываем строку json в объект Python
        resp = json.loads(r.content)
        # Расчитываем стоимость n количества запрошенной валюты
        new_price = resp[quote_key] * amount
        # Округляем до 3 знаком после запятой
        new_price = round(new_price, 3)
        # Выводим сообщение
        message = f"Цена за {amount} {base} : {new_price} {quote}"
        return message
