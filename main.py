import telebot
from config import TOKEN,keys
from extensions import CurrencyConverter, APIException
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help_command(message: telebot.types.Message):
    text = (
        "Чтобы узнать цену валюты, отправьте сообщение в формате:\n"
        "<валюта_из> <валюта_в> <количество>\n"
        "Пример: юань рубль 159 \n\n"
        "Доступные команды:\n"
        "/start, /help — инструкция\n"
        "/values — показать список поддерживаемых валют"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values_command(message: telebot.types.Message):
    text = "Поддерживаемые валюты:\n" + "\n".join(f"- {k} ({v})" for k, v in keys.items())
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert_currency(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Неверный формат.\n Пример: доллар рубль 200")

        base, quote, amount = values
        base = base.strip().lower()
        quote = quote.strip().lower()

        if base not in keys:
            raise APIException(f"Валюта '{base}' не поддерживается.")
        if quote not in keys:
            raise APIException(f"Валюта '{quote}' не поддерживается.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Количество должно быть числом.")

        if amount <= 0:
            raise APIException("Количество должно быть больше нуля.")

        base_code = keys[base]
        quote_code = keys[quote]

        result = CurrencyConverter.get_price(base_code, quote_code, amount)
        text = f"{amount} {base} = {result:.2f} {quote}"

    except APIException as e:
        text = f"Ошибка: {e}"
    except Exception as e:
        text = f"Неизвестная ошибка: {e}"

    bot.reply_to(message, text)


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)