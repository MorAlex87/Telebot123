import requests
import json
from config import API_KEY

class APIException(Exception):
    """Исключение для ошибок API и ввода пользователя."""
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        if base == quote:
            raise APIException(f"Невозможно конвертировать {base} в ту же валюту.")
        try:
            if not isinstance(amount, (int, float)):
                amount = float(amount)
            if amount <= 0:
                raise APIException("Количество должно быть больше нуля.")
        except (ValueError, TypeError):
            raise APIException(f"Количество должно быть числом. Получено: {amount}")
        #Формирование URL
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base}/{quote}/{amount}"
        #Отправка запроса
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise APIException(
                f"Ошибка API: HTTP {response.status_code}. "
                f"Ответ сервера: {response.text[:200]}"
            )
        content_type = response.headers.get('content-type', '').lower()
        if 'application/json' not in content_type:
            raise APIException(
                f"Неверный Content-Type: {content_type}. "
                f"Ожидался application/json. Ответ: {response.text[:200]}"
            )
        if not response.text.strip():
            raise APIException("Пустой ответ от сервера.")
        data = json.loads(response.text)

        return data["conversion_result"]